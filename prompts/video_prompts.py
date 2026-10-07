"""
System prompt and task templates for the **Video Production Agent**.

The Video Production Agent focuses on video storytelling and
pre-production materials: scripts, storyboards, shot lists,
voice-over scripts, and social media video concepts.
"""

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

VIDEO_SYSTEM_PROMPT = """
You are a professional video production assistant.
Return ONLY valid JSON matching the required schema.
Never reveal your reasoning, analysis, planning, calculations, drafting process, or internal thoughts.
Do not explain how you generated the answer.
Do not include markdown, code fences, explanations, or any text before or after the JSON.
The response must begin with { and end with }.

Your video production strengths are:
- Strong narrative structure (setup, conflict, resolution)
- Visual storytelling that complements audio
- Platform-specific format awareness (YouTube, TikTok, Instagram)
- Clear scene breakdowns with timing estimates
- Collaborative and director-friendly language

Always produce practical, production-ready materials.
"""

# ---------------------------------------------------------------------------
# Task templates
# ---------------------------------------------------------------------------

VIDEO_SCRIPT_TEMPLATE = """
Write a video script for the following:

Video topic: {topic}
Video type: {video_type} (e.g. explainer, tutorial, documentary, ad)
Target length: approximately {duration} seconds
Target audience: {target_audience}
Tone: {tone}
Call to Action (CTA): {cta}

Structure the script as follows:
1. An opening hook (0-10 seconds)
2. An introduction / main topic reveal (10-20 seconds)
3. Body content with clear scene breakdowns (use S1, S2, S3 etc.)
4. A conclusion / call-to-action (last 10-15 seconds)

For each scene include:
- Scene number and rough timestamp
- Visual description (what the viewer sees)
- Dialogue / narration text
- Camera / audio notes

Return the result as a JSON object with this exact schema:
{
  "title": "Video title",
  "hook": "Opening hook text",
  "script": "Full script text",
  "scenes": [
    {
      "scene": "S1",
      "timestamp": "0:00-0:05",
      "visual": "Description of visual",
      "voiceover": "Narration text",
      "camera": "Camera notes",
      "audio": "Audio notes"
    }
  ],
  "storyboard": [
    {
      "scene": "S1",
      "visual": "Visual description",
      "on_screen_text": "Any on-screen text"
    }
  ],
  "shot_list": [
    {
      "shot": "1",
      "description": "Shot description",
      "camera": "Camera details"
    }
  ],
  "voiceover": "Full voice-over script",
  "on_screen_text": "Key on-screen text elements",
  "cta": "Call to action text"
}

Provide only the JSON.
"""

STORYBOARD_TEMPLATE = """
Create a storyboard for a {duration}-second video with the following
concept:

Video topic: {topic}
Target audience: {target_audience}
Tone: {tone}
Call to Action (CTA): {cta}

For each scene (aim for {scene_count} scenes), provide:
1. Scene number and frame number
2. A visual description (what is drawn / filmed)
3. Dialogue / narration (if any)
4. Camera angle / movement notes
5. On-screen text (if any)

Return the result as a JSON object with this exact schema:
{
  "title": "Storyboard title",
  "storyboard": [
    {
      "scene": "S1",
      "visual": "Visual description",
      "on_screen_text": "Any on-screen text"
    }
  ],
  "cta": "Call to action text"
}

Provide only the JSON.
"""

SHOT_LIST_TEMPLATE = """
Create a detailed shot list for a video shoot based on:

Video topic: {topic}
Video type: {video_type}
Target length: {duration} seconds
Target audience: {target_audience}
Camera available: {camera}
Call to Action (CTA): {cta}

Include a table with columns:
- Shot #
- Shot type (e.g. Wide, Medium, Close-up)
- Description
- Duration (seconds)
- Audio notes
- Notes

Provide at least 10 shots covering the full video.

Return the result as a JSON object with this exact schema:
{
  "title": "Shot list title",
  "shot_list": [
    {
      "shot": "1",
      "description": "Shot description",
      "camera": "Camera details",
      "audio": "Audio notes",
      "notes": "Additional notes"
    }
  ],
  "cta": "Call to action text"
}
"""

VOICEOVER_SCRIPT_TEMPLATE = """
Write a professional voice-over script for a {duration}-second video
on the topic:

Video topic: {topic}
Target audience: {target_audience}
Tone: {tone}
Call to Action (CTA): {cta}

Present the script as clean narration text, organised by scene or
beat. Include timing cues (e.g. [0:00-0:08]) and brief production
directions in brackets (e.g. [pause], [emphasise]).

Return the result as a JSON object with this exact schema:
{
  "title": "Voice-over script title",
  "voiceover": "Full voice-over script text with timing cues",
  "cta": "Call to action text"
}

Provide only the JSON.
"""

SOCIAL_MEDIA_VIDEO_TEMPLATE = """
Create social media video concepts for {platform} based on:

Topic: {topic}
Target product/service: {product}
Target audience: {target_audience}
Tone: {tone}
Call to Action (CTA): {cta}

Produce 3 distinct video concepts. For each concept include:
1. A hook / first-frame idea (first 3 seconds)
2. A brief storyline (3-5 scenes)
3. Caption text (with relevant hashtags)
4. Suggested on-screen text overlays
5. Call-to-action

Return the result as a JSON object with this exact schema:
{
  "title": "Social media video concepts",
  "hook": "Main hook idea",
  "script": "Brief storyline",
  "scenes": [
    {
      "scene": "Scene 1",
      "visual": "Visual description",
      "voiceover": "Voice-over text"
    }
  ],
  "cta": "Call to action text"
}

Provide only the JSON.
"""
