"""
Reusable OpenRouter API client.

This module provides a thin, centralized wrapper around the OpenRouter
API. It loads the API key and model name from environment variables,
validates the configuration, and exposes a single ``generate`` method
that every agent in the project calls.

Environment variables
---------------------
OPENROUTER_API_KEY   (required)  Your OpenRouter API key.
OPENROUTER_MODEL     (optional)  Model name to use. Defaults to
                                  ``nvidia/nemotron-3.5-lightning:free``.
"""

import json
import os
import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "nvidia/nemotron-3.5-lightning:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterClient:
    """A minimal wrapper around the OpenRouter API used by all agents."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is required. Set the environment variable "
                "or pass it explicitly."
            )

        self.model_name = model or os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)

    def check_connection(self) -> tuple[bool, str]:
        try:
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": "Respond with exactly: OK"}],
                "max_tokens": 5,
            }
            headers = self._build_headers()
            with httpx.Client(timeout=15.0) as client:
                response = client.post(
                    OPENROUTER_API_URL,
                    json=payload,
                    headers=headers,
                )
            if response.status_code == 200:
                data = response.json()
                message = data.get("choices", [{}])[0].get("message", {})
                text = message.get("content", "").strip()
                if text:
                    return (True, f"Connected to OpenRouter ({self.model_name})")
                return (False, "OpenRouter returned an empty response.")
            return self._handle_error_response(response)
        except httpx.ConnectionError:
            return (False, "Unable to connect to OpenRouter. Check your internet connection.")
        except httpx.TimeoutException:
            return (False, "OpenRouter request timed out. Try again.")
        except Exception as exc:
            return (False, f"Unexpected error connecting to OpenRouter: {exc}")

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not configured. Add it to your .env file."
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        headers = self._build_headers()

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    OPENROUTER_API_URL,
                    json=payload,
                    headers=headers,
                )
            if response.status_code == 200:
                data = response.json()
                message = data.get("choices", [{}])[0].get("message", {})
                text = message.get("content", "").strip()
                if not text:
                    raise RuntimeError("Received an empty response from OpenRouter.")
                cleaned = self.extract_final_response(data)
                if not cleaned:
                    raise RuntimeError("Received an empty response after cleaning.")
                return cleaned
            raise RuntimeError(self._handle_error_response(response)[1])
        except httpx.ConnectionError:
            raise RuntimeError(
                "Unable to connect to OpenRouter. Check your internet connection."
            )
        except httpx.TimeoutException:
            raise RuntimeError(
                "OpenRouter request timed out. The model may be under heavy load."
            )
        except RuntimeError:
            raise
        except Exception as exc:
            logger.error("OpenRouter API call failed: %s", exc)
            raise RuntimeError(f"Unexpected error calling OpenRouter: {exc}") from exc

    def _build_headers(self) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        http_referer = os.environ.get("OPENROUTER_HTTP_REFERER")
        x_title = os.environ.get("OPENROUTER_X_TITLE")
        if http_referer:
            headers["HTTP-Referer"] = http_referer
        if x_title:
            headers["X-Title"] = x_title
        return headers

    def _handle_error_response(self, response: httpx.Response) -> tuple[bool, str]:
        status = response.status_code
        try:
            data = response.json()
            error_msg = data.get("error", {}).get("message", response.text)
        except Exception:
            error_msg = response.text

        if status == 401:
            return (False, "Invalid OpenRouter API key.")
        if status == 402:
            return (False, "This model/request requires payment or the free model is currently unavailable.")
        if status == 429:
            return (False, "OpenRouter rate limit reached. Please try again later.")
        if status in (500, 502, 503):
            return (False, "OpenRouter is temporarily unavailable. Please try again later.")
        return (False, f"OpenRouter API error ({status}): {error_msg}")

    @staticmethod
    def extract_final_response(data: dict) -> str:
        """
        Extract only the final assistant content from an OpenRouter API
        response, discarding any reasoning/thinking/analysis fields.

        Parameters
        ----------
        data : dict
            The parsed JSON response from OpenRouter.

        Returns
        -------
        str
            The cleaned final assistant content.
        """
        message = data.get("choices", [{}])[0].get("message", {})
        text = message.get("content", "").strip()
        if not text:
            return ""
        cleaned = OpenRouterClient._strip_all_reasoning(text)
        return cleaned.strip()

    @staticmethod
    def _strip_all_reasoning(text: str) -> str:
        """
        Remove internal reasoning, chain-of-thought, analysis, planning,
        and drafting sections from model output.

        This handles:
        - Lines that start with common reasoning markers
        - Multi-line reasoning blocks
        - Reasoning embedded within the content
        """
        reasoning_phrases = [
            "analyze user request",
            "analyze user input",
            "deconstruct requirements",
            "determine output structure",
            "determine strategy",
            "let's outline",
            "let me outline",
            "let's draft",
            "drafting",
            "let's count",
            "let me count",
            "let me re-read",
            "actually,",
            "let me reinterpret",
            "here's a thinking process",
            "here is a thinking process",
            "thinking process:",
            "analysis:",
            "reasoning:",
            "internal reasoning:",
            "chain-of-thought:",
            "let me think through this",
            "let me analyze",
            "step 1:",
            "step 2:",
            "step 3:",
            "first, i'll",
            "next, i'll",
            "finally, i'll",
            "thinking:",
            "wait...",
            "wait,",
            "i need to make sure",
            "i need to",
            "let me plan",
            "let me think",
            "let's think",
            "let me allocate",
            "let me make sure",
            "let me draft",
            "let me start",
            "let me begin",
            "let me first",
            "let me now",
            "let me check",
            "let me verify",
            "planning:",
            "draft:",
            "drafting:",
            "outline:",
            "structuring:",
            "organizing:",
            "organizing the",
            "structuring the",
            "breaking down",
            "breaking this down",
            "let me break",
            "let me consider",
            "considering",
            "re-reading",
            "rereading",
            "let's re-read",
            "let me re-read",
            "thinking about",
            "thought process",
            "my thinking",
            "internal thought",
            "private reasoning",
            "monologue:",
            "self-correction:",
            "correction:",
            "actually i",
            "actually, i",
            "wait -",
            "wait.",
            "let me rewrite",
            "check primary text",
            "check characters",
            "counting characters",
            "counting chars",
            "let me count",
            "let me check chars",
            "checking characters",
            "character count",
            "revise",
            "revising",
            "improve",
            "improving",
            "refine",
            "refining",
            "optimize",
            "optimizing",
            "finalize",
            "finalizing",
            "polish",
            "polishing",
            "rewrite",
            "rewriting",
            "adjust",
            "adjusting",
            "tweak",
            "tweaking",
            "shorten",
            "lengthen",
            "trim",
            "trimming",
            "edit",
            "editing",
        ]

        lines = text.splitlines()
        cleaned = []
        skip_mode = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            lower_stripped = stripped.lower()

            if not skip_mode:
                if any(lower_stripped.startswith(p) for p in reasoning_phrases):
                    skip_mode = True
                    continue
                cleaned.append(line)
            else:
                if not stripped:
                    skip_mode = False
                    cleaned.append(line)
                elif any(lower_stripped.startswith(p) for p in reasoning_phrases):
                    continue
                elif lower_stripped.startswith("#") or lower_stripped.startswith("**") or lower_stripped.startswith("- ") or lower_stripped.startswith("|"):
                    skip_mode = False
                    cleaned.append(line)
                elif len(stripped) > 100:
                    skip_mode = False
                    cleaned.append(line)
                else:
                    continue

        result = "\n".join(cleaned).strip()

        if not result:
            return text.strip()

        return result

    @staticmethod
    def extract_json_text(text: str) -> dict:
        """
        Extract structured JSON from model output text.

        Steps:
        1. Strip whitespace.
        2. Remove accidental markdown code fences.
        3. Find first ``{`` and last ``}``.
        4. Parse using ``json.loads``.
        5. Return the dictionary.

        Parameters
        ----------
        text : str
            Raw model output text.

        Returns
        -------
        dict
            Parsed JSON object.

        Raises
        ------
        ValueError
            If no valid JSON object can be extracted.
        """
        if not text or not text.strip():
            raise ValueError("Empty response text.")

        cleaned = text.strip()

        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()

        json_start = cleaned.find("{")
        json_end = cleaned.rfind("}")
        if json_start != -1 and json_end != -1 and json_end > json_start:
            cleaned = cleaned[json_start:json_end + 1]

        try:
            parsed = json.loads(cleaned)
            if not isinstance(parsed, dict):
                raise ValueError("JSON root must be an object")
            return parsed
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"Failed to parse JSON from response: {exc}") from exc
