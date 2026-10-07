"""
System prompt and task templates for the **Copywriting & Ads Agent**.

The Copywriting & Ads Agent specialises in short-form, persuasive, and
conversion-focused writing for paid-ad campaigns, product descriptions,
email marketing, and call-to-action optimisation.
"""

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

COPYWRITING_SYSTEM_PROMPT = """
You are a professional Copywriting & Ads Agent. Your expertise spans
Facebook Ads, Google Ads, LinkedIn Ads, product descriptions, email
copy, and call-to-action (CTA) variations.

Your copywriting strengths are:
- Persuasive and benefit-driven messaging
- Strong command of AIDA (Attention, Interest, Desire, Action)
- Platform-specific best practices and character limits
- Audience-first language with emotional triggers
- Clear, compelling CTAs

CRITICAL RULES:
- NEVER display your reasoning, thinking process, analysis, planning, or character-count calculations.
- Return ONLY valid JSON matching the required schema.
- Do not include phrases like "Here's my analysis", "Step 1", "First I'll", "I'll now", or any chain-of-thought.
- Do not count characters in your response.
- Do not explain how you created the ads.
- Do not include markdown, code fences, explanations, or any text before or after the JSON.
- The response must begin with { and end with }.

Always produce copy that drives clicks, engagement, and conversions.
"""

# ---------------------------------------------------------------------------
# Task templates
# ---------------------------------------------------------------------------

FACEBOOK_ADS_TEMPLATE = """
Write Facebook ad copy for the following product/service:

Product/Service: {product}
Platform: {platform}
Campaign Objective: {campaign_objective}
Key benefits: {benefits}
Target audience: {target_audience}
Tone: {tone}

Return ONLY valid JSON with this exact schema:
{
  "variations": [
    {
      "primary_text": "Primary text (max 90 characters)",
      "headline": "Headline (max 40 characters)",
      "description": "Description (max 30 characters)",
      "cta": "Call to action (3-6 words)"
    },
    {
      "primary_text": "...",
      "headline": "...",
      "description": "...",
      "cta": "..."
    },
    {
      "primary_text": "...",
      "headline": "...",
      "description": "...",
      "cta": "..."
    }
  ]
}

Do not count characters in your response.
Do not explain how you created the ads.
Return only the final 3 ad variations.
"""

GOOGLE_ADS_TEMPLATE = """
Write Google Search ad copy for the following:

Product/Service: {product}
Platform: {platform}
Campaign Objective: {campaign_objective}
Target keyword: {keyword}
Target audience: {target_audience}
Tone: {tone}
Final URL: {url}

Return ONLY valid JSON with this exact schema:
{
  "variations": [
    {
      "headlines": ["Headline 1", "Headline 2", "Headline 3"],
      "descriptions": ["Description 1", "Description 2"],
      "final_url": "https://example.com"
    },
    {
      "headlines": ["...", "...", "..."],
      "descriptions": ["...", "..."],
      "final_url": "..."
    },
    {
      "headlines": ["...", "...", "..."],
      "descriptions": ["...", "..."],
      "final_url": "..."
    }
  ]
}

Do not count characters in your response.
Do not explain how you created the ads.
Return only the final 3 ad variations.
"""

LINKEDIN_ADS_TEMPLATE = """
Write LinkedIn ad copy for the following B2B offering:

Product/Service: {product}
Platform: {platform}
Campaign Objective: {campaign_objective}
Key benefits: {benefits}
Target audience (job titles/industries): {target_audience}
Tone: {tone}

Return ONLY valid JSON with this exact schema:
{
  "variations": [
    {
      "headline": "Headline (max 70 characters)",
      "body": "Body text (brief and professional)",
      "cta": "CTA button text (e.g. Learn More, Get Started)"
    },
    {
      "headline": "...",
      "body": "...",
      "cta": "..."
    },
    {
      "headline": "...",
      "body": "...",
      "cta": "..."
    }
  ]
}

Do not count characters in your response.
Do not explain how you created the ads.
Return only the final 3 ad variations.
"""

PRODUCT_DESCRIPTION_TEMPLATE = """
Write product descriptions for the following product:

Product name: {product_name}
Platform: {platform}
Campaign Objective: {campaign_objective}
Category: {category}
Key features: {features}
Target audience: {target_audience}
Tone: {tone}

Return ONLY valid JSON with this exact schema:
{
  "title": "Product title (under 60 characters)",
  "meta_description": "Meta description (under 160 characters)",
  "full_description": "Full product description (3-4 short paragraphs)",
  "bullet_points": ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"]
}

Do not explain how you created the descriptions.
Return only the final product description sections.
"""

EMAIL_COPY_TEMPLATE = """
Write an email campaign for the following purpose:

Purpose: {purpose}
Product/Service: {product}
Platform: {platform}
Campaign Objective: {campaign_objective}
Target audience: {target_audience}
Tone: {tone}

Return ONLY valid JSON with this exact schema:
{
  "subject": "Subject line (under 50 characters)",
  "preheader": "Pre-header text (under 100 characters)",
  "body": "Email body with greeting, intro, main message, CTA",
  "ps": "Post-script line"
}

Do not explain how you created the email.
Return only the final email copy.
"""

CTA_VARIATIONS_TEMPLATE = """
Generate at least 5 distinct call-to-action (CTA) button texts for the
following context:

Product/Service: {product}
Platform: {platform}
Campaign Objective: {campaign_objective}
Goal / desired action: {action}
Target audience: {target_audience}
Tone: {tone}

Return ONLY valid JSON with this exact schema:
{
  "ctas": ["CTA 1", "CTA 2", "CTA 3", "CTA 4", "CTA 5"]
}

Do not explain how you created the CTAs.
Return only the final CTA list.
"""
