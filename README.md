# AI Agent Assignment

A professional, multi-agent AI workspace built with **Python** and **Streamlit**. It features three specialised AI agents — each with its own system prompt, workflow, and demo outputs — that leverage **OpenRouter** for content generation using the free **NVIDIA Nemotron 3.5 Lightning** model. A built-in **Demo Mode** lets you showcase every agent without an API key, making it perfect for interviews and demos.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Environment Variable Setup](#environment-variable-setup)
7. [OpenRouter API Key Setup](#openrouter-api-key-setup)
8. [How to Run in VS Code (Windows)](#how-to-run-in-vs-code-windows)
9. [Agent Details](#agent-details)
10. [Demo Mode](#demo-mode)
11. [Example Inputs](#example-inputs)
12. [Example Outputs](#example-outputs)
13. [Troubleshooting](#troubleshooting)

---

## Overview

This project provides a clean, modular web application where a user can select from three distinct AI agents:

| Agent | Specialisation |
|-------|---------------|
| **Content Writing Agent** | Blogs, website content, e-book chapters, SEO articles |
| **Copywriting & Ads Agent** | Facebook/Google/LinkedIn ads, product descriptions, email copy, CTAs |
| **Video Production Agent** | Video scripts, storyboards, shot lists, voice-over scripts, social media concepts |

All agents use **OpenRouter** with the free model `nvidia/nemotron-3.5-lightning:free`. API keys are loaded exclusively from environment variables — **never hardcoded**.

---

## Features

- **Three completely separate agents** — each with its own system prompt, task templates, and workflow.
- **Reusable OpenRouter client** — a single `OpenRouterClient` class handles all API communication, error handling, and model configuration.
- **Environment variable configuration** — API key and model loaded from `.env`, never exposed in source.
- **Professional Streamlit UI** — sidebar agent selector, OpenRouter mode toggle, test connection button, agent-specific input forms, clean markdown output.
- **Copy / Download functionality** — one-click copy-to-clipboard and download-as-`.md` for every result.
- **Comprehensive error handling** — graceful messages for missing API keys, rate limits, API failures, and empty inputs.
- **Demo Mode** — predefined sample outputs for all three agents (3 samples each), clearly labelled as demo data.
- **Modular architecture** — prompts, agents, and utilities are cleanly separated.

---

## Architecture

```
app.py  ──►  Streamlit UI layer
             │
             │  (imports & instantiates)
             ▼
┌────────────┬─────────────┬─────────────┐
│ Agents/    │ Prompts/    │ Utils/      │
│            │             │             │
│ content    │ content_    │ openrouter_ │
│ _agent.py  │ prompts.py  │ client.py   │
│            │             │             │
│ copywriting│ copywriting │             │
│ _agent.py  │ _prompts.py │             │
│            │             │             │
│ video_     │ video_      │             │
│ agent.py   │ prompts.py  │             │
└────────────┴─────────────┴─────────────┘
```

### Data Flow

1. The user selects an agent and mode (Demo / OpenRouter) in the **sidebar**.
2. The main app renders agent-specific input fields.
3. On "Generate":
   - **Demo Mode**: The agent returns a pre-written sample from `DEMO_OUTPUTS`.
   - **OpenRouter Mode**: The agent builds a prompt using its template, sends it to `OpenRouterClient`, and returns the API response.
4. The result is rendered in a styled output container with **copy** and **download** buttons.

### Key Design Decisions

- **`OpenRouterClient`** is the single point of contact with the OpenRouter API. It centralises API key validation, model selection, and error handling.
- **Prompt templates** live in `prompts/` and are pure string templates. This keeps the "what to ask the LLM" logic separate from "how to ask the LLM".
- **Agents** (`agents/*.py`) contain both the demo data (3 samples per type) and the `generate()` method that orchestrates prompt → API call → result.
- **No API key is ever hardcoded**. The key is read from `OPENROUTER_API_KEY` via `python-dotenv`.
- **Demo mode** is fully separate from real API calls. Demo outputs are clearly labelled and never claimed to be OpenRouter-generated.

---

## Project Structure

```
ai-agent-assignment/
│
├── app.py                    # Main Streamlit application (UI)
├── requirements.txt          # Python dependencies
├── .env.example              # Template for environment variables
├── .env                      # Your actual key (created at setup, NOT committed)
├── .gitignore                # Git ignore rules
├── README.md                 # This file
│
├── agents/                   # Agent logic — each agent is a standalone module
│   ├── __init__.py
│   ├── content_agent.py      # Content Writing Agent
│   ├── copywriting_agent.py  # Copywriting & Ads Agent
│   └── video_agent.py        # Video Production Agent
│
├── prompts/                  # Prompt templates & system prompts
│   ├── __init__.py
│   ├── content_prompts.py    # System prompt + 4 content templates
│   ├── copywriting_prompts.py# System prompt + 6 copy templates
│   └── video_prompts.py      # System prompt + 5 video templates
│
└── utils/                    # Shared utilities
    ├── __init__.py
    └── openrouter_client.py  # Reusable OpenRouter API wrapper
```

---

## Installation

### Prerequisites

- **Python 3.9+** (3.11+ recommended)
- **pip** (comes with Python)
- **VS Code** with the Python extension installed
- An **OpenRouter API key** (for OpenRouter Mode — get one at [OpenRouter](https://openrouter.ai/keys))

### Step-by-Step

1. **Clone or copy the project** to your workspace (e.g. `F:\ai-agent-assignment`).

2. **Open the project folder in VS Code.**

   ```
   File → Open Folder → Select `ai-agent-assignment`
   ```

3. **Create a virtual environment:**

   ```powershell
   python -m venv .venv
   ```

4. **Activate the virtual environment:**

   ```powershell
   .venv\Scripts\activate
   ```

   You should see `(.venv)` appear at the start of your terminal prompt.

5. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

---

## Environment Variable Setup

The app reads your OpenRouter API key from a `.env` file (loaded via `python-dotenv`).

1. **Copy the example file:**

   ```powershell
   copy .env.example .env
   ```

2. **Open `.env`** in VS Code and replace the placeholder with your real key:

 ```env
 OPENROUTER_API_KEY=sk-or-...your_real_key_here
 OPENROUTER_MODEL=nvidia/nemotron-3.5-lightning:free
 ```

   > **⚠️ Security:** Never commit `.env` to version control. It is included in `.gitignore`.

3. **Verify the key is loaded** (optional check):

   ```powershell
   echo $env:OPENROUTER_API_KEY
   ```

---

## OpenRouter API Key Setup

Before using **OpenRouter Mode**, you must obtain an API key from OpenRouter.

1. **Go to OpenRouter:**
   https://openrouter.ai/keys

2. **Sign in** with your Google or GitHub account.

3. **Create an API key** by clicking **"Create Key"**.

4. **Copy the key** and paste it into your `.env` file as `OPENROUTER_API_KEY`.

5. **Verify the key works** by running the app and switching to **OpenRouter Mode** in the sidebar.

---

## How to Run in VS Code (Windows)

1. **Open the project folder** in VS Code (`File → Open Folder`).

2. **Open the integrated terminal** in VS Code:

   ```
   View → Terminal      (or press `` Ctrl + ` ``)
   ```

3. **Run the full setup sequence:**

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. **A browser tab** will automatically open at `http://localhost:8501`.

5. **Stop the app:** Press `Ctrl + C` in the terminal, then `y` to confirm.

---

## Agent Details

### 1. Content Writing Agent

**System Prompt Focus:** Informative, SEO-friendly, well-structured long-form content.

**Workflow:**
User Topic → Target Audience → Tone → Content Type → Generate Outline → Generate Content → SEO Optimization → Quality Check → Final Output

**Supported Types:**

| Type | Description |
|------|-------------|
| Blog Post | Full blog with hook, sections, FAQ, and CTA |
| Website Content | Headline, subheadline, hero, benefits, about, CTA |
| E-book Content | Chapter with sections, examples, exercises, summary |
| SEO Article | SEO title, meta description, primary/secondary keywords, H1/H2/H3 headings, article body, conclusion |

**Demo Outputs (3 each):**
- 3 blog post samples (morning routine, remote team management, sustainable living)
- 3 website content samples (SaaS product, coffee roaster, meditation app)
- 3 e-book chapter samples (marketing funnel, email list growth, SEO writing)

---

### 2. Copywriting & Ads Agent

**System Prompt Focus:** Persuasive, conversion-driven short-form copy using AIDA.

**Workflow:**
Product/Service → Target Audience → Pain Point → Value Proposition → Platform → Generate Marketing Copy → CTA Variations → Quality Check → Final Output

**Supported Types:**

| Type | Description |
|------|-------------|
| Facebook Ads | 3 ad variations with primary text, headline, description, CTA |
| Google Ads | 3 responsive search ad variations with headlines + descriptions |
| LinkedIn Ads | 3 B2B ad variations with headline, body, CTA button |
| Product Description | Title, meta, full description, Amazon-style bullets |
| Email Copy | Subject, preview, body, P.S. |
| CTA Variations | 10 distinct CTA button texts |

**Demo Outputs (3 each):**
- 3 Facebook ad sets (fitness app, skincare, online course)
- 3 Google ad sets (home security, CRM software, chef knives)
- 3 LinkedIn ad sets (lead gen, cloud backup, consulting)
- 3 product descriptions (office chair, vitamin C serum, hybrid bike)
- 3 email campaigns (webinar invite, product launch, newsletter)
- 3 CTA variation sets (productivity app, e-commerce checkout, course enrolment)

---

### 3. Video Production Agent

**System Prompt Focus:** Visual storytelling, production-ready deliverables.

**Workflow:**
Video Topic → Target Audience → Platform → Duration → Generate Hook → Generate Script → Scene Breakdown → Storyboard → Shot List → Voice-over Script → CTA

**Supported Types:**

| Type | Description |
|------|-------------|
| Video Script | Scene-by-scene script with timestamps, visuals, V.O. |
| Storyboard | Scene-by-frame visual description, dialogue, camera notes |
| Shot List | Table of shots with type, description, duration, audio, notes |
| Voice-Over Script | Timed narration with visual direction cues |
| Social Media Video | 3 concept ideas with hook, storyline, caption, overlays |

**Demo Outputs (3 each):**
- 3 video scripts (product demo, documentary short, fitness routine)
- 3 storyboards (public transport ad, tech comedy, coffee commercial)
- 3 shot lists (app demo, interview, yoga flow)
- 3 voice-over scripts (urban greening, heist thriller, science of flavour)
- 3 social media video concept sets (desk workout, tech tips, knife skills)

---

## Demo Mode

### How It Works

- **Demo Mode** (default) uses pre-written sample outputs stored in each agent module.
- The sidebar lets you switch between **Demo Mode** and **OpenRouter Mode**.
- In Demo Mode, you can also cycle through **Demo Output 1, 2, or 3** for each content type.
- A prominent **info banner** and **sidebar indicator** show when Demo Mode is active.
- Every demo output includes a footer: `*Demo Output – not generated by AI*`

### Why Demo Mode?

- **No API key required** — perfect for interviews and presentations.
- **Consistent, reliable outputs** — always available and correctly formatted.
- **Showcases the full range** of each agent's capabilities.
- **Zero latency** — instant results for smooth demos.

### Switching Modes

1. In the **sidebar**, select **OpenRouter Mode**.
2. Ensure `OPENROUTER_API_KEY` is set in `.env`.
3. Click "Generate" — the app will call the OpenRouter API.

---

## Example Inputs

### Content Writing Agent — Blog Post

| Field | Example |
|-------|---------|
| Content Type | Blog Post |
| Topic | "The Future of Remote Work in 2025" |
| Target Audience | "Tech industry leaders and HR managers" |
| Tone | "Professional" |
| Word Count | 2000 |
| Keywords | "remote work, hybrid teams, productivity" |
| Additional Context | "Include statistics, 3 actionable strategies, and a case study" |

### Copywriting & Ads Agent — LinkedIn Ads

| Field | Example |
|-------|---------|
| Content Type | LinkedIn Ads |
| Product / Service | "CloudSecure Backup" |
| Platform | LinkedIn |
| Target Audience | "IT managers at mid-market companies" |
| Campaign Objective | Lead Generation |
| Tone | "Professional" |
| Key Benefit | "99.99% uptime, GDPR compliant, 1-click restore" |

### Video Production Agent — Video Script

| Field | Example |
|-------|---------|
| Content Type | Video Script |
| Video Topic | "EcoBot – Sustainable Cleaning Robot" |
| Platform | YouTube |
| Target Duration | "45 seconds" |
| Target Audience | "Eco-conscious homeowners, 30–50" |
| Video Style | "Inspirational" |
| CTA | "Visit our website to learn more" |

---

## Example Outputs

Each agent provides 3 sample outputs in Demo Mode. Here are brief previews:

### Content Writing — Blog Post Sample

```markdown
# How to Build a Successful Morning Routine

## Introduction

Starting your day right can be the difference between feeling overwhelmed and feeling in control. A well-structured morning routine sets the tone for productivity, mental clarity, and overall well-being.
```

### Copywriting — Facebook Ads Sample

```markdown
# Facebook Ad Variations – FitTrack Pro

## Variation 1

**Primary Text:** Transform your body in 30 days. FitTrack Pro gives you personalised workouts that fit your schedule. Download now and get 50% off!

**Headline:** 30-Day Fitness Transformation

**CTA:** Shop Now
```

### Video Production — Video Script Sample

```markdown
# Video Script – "The Morning Stack" (60-second product demo)

### [0:00–0:04] Opening Hook
**Visual:** Fast-paced montage – alarm clock, coffee brewing, emails flooding inbox.
**Voice-over (V.O.):** "Tired of starting your day in firefighting mode?"
```

---

## Troubleshooting

### "Invalid OpenRouter API key"

1. Verify your key at https://openrouter.ai/keys.
2. Ensure there are no extra spaces or quotes in `.env`.
3. Regenerate the key if needed and update `.env`.

### "OpenRouter rate limit reached (429)"

1. Wait a few minutes before retrying.
2. Check your usage at https://openrouter.ai/keys.
3. The free model `nvidia/nemotron-3.5-lightning:free` has its own rate limits.

### "OpenRouter is temporarily unavailable (500/502/503)"

1. OpenRouter may be experiencing high demand. The app will display a clear message.
2. Wait a few seconds and try again.
3. If the issue persists, switch to **Demo Mode** temporarily.

### "OPENROUTER_API_KEY is not configured"

1. Copy `.env.example` to `.env`.
2. Add your OpenRouter API key: `OPENROUTER_API_KEY=sk-or-...`.
3. Restart the Streamlit app: `Ctrl + C` then `streamlit run app.py`.

### "ModuleNotFoundError: No module named 'agents'"

- Make sure you're running the app from the project root directory.
- Verify the virtual environment is activated: `.venv\Scripts\activate`.

### Streamlit won't start / port already in use

```powershell
streamlit run app.py --server.port 8502
```

### Output looks garbled (not rendering markdown)

- Ensure you're using **Streamlit 1.38+** (specified in `requirements.txt`).
- Update if needed: `pip install --upgrade streamlit`.

---

## License

This project is provided for educational and demonstration purposes.

---

*Made with ❤️ using Python, Streamlit, and OpenRouter.*
