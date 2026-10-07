"""
System prompt and task templates for the **Content Writing Agent**.

The Content Writing Agent focuses on long-form, informative, and
SEO-friendly written content such as blog posts, website copy,
e-book chapters, and SEO articles.
"""

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
# This is the personality / behavioural instruction that the LLM receives
# at the start of every request.  It is kept separate from the dynamic
# task templates below for clarity and modularity.

CONTENT_SYSTEM_PROMPT = """
You are a professional Content Writing Agent. Your expertise spans
blog writing, website content, e-book authorship, and SEO-optimized
article creation.

Your writing style is:
- Clear, engaging, and audience-focused
- Well-structured with headings, sub-headings, and logical flow
- SEO-friendly with natural keyword integration
- Adaptable to different industries and target audiences
- Accurate with proper tone and voice

CRITICAL RULES:
- NEVER display your reasoning, thinking process, analysis, planning, or word-count calculations.
- Return ONLY valid JSON matching the required schema.
- Do not include phrases like "Here's my analysis", "Step 1", "First I'll", "I'll now", or any chain-of-thought.
- Do not count words in your response.
- Do not explain how you created the content.
- Do not include markdown, code fences, explanations, or any text before or after the JSON.
- The response must begin with { and end with }.

Always produce high-quality, original content that provides real value
to readers.
"""

# ---------------------------------------------------------------------------
# Task templates
# ---------------------------------------------------------------------------
# Each template takes a topic / keyword and optional context, then
# returns a full prompt string to send to the LLM.

BLOG_POST_TEMPLATE = """
Write a comprehensive, well-researched blog post on the topic: "{topic}".

Target audience: {target_audience}
Tone: {tone}
Desired length: approximately {word_count} words.
Keywords to include naturally: {keywords}

Return ONLY valid JSON with this exact schema:
{
  "title": "Compelling blog post title",
  "content": "Full blog post content with markdown headings, body text, bullet points, and FAQ section"
}

Do not count words in your response.
Do not explain how you created the content.
Return only the final blog post.
"""

WEBSITE_CONTENT_TEMPLATE = """
You are writing website copy for a {content_type} page.

Business / brand: {brand_name}
Industry: {industry}
Target audience: {target_audience}
Tone: {tone}

Return ONLY valid JSON with this exact schema:
{
  "headline": "Headline (under 70 characters for SEO)",
  "subheadline": "Subheadline that reinforces the headline",
  "hero": "Hero paragraph (2-3 sentences, punchy)",
  "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
  "about": "Brief About section (2-3 paragraphs)",
  "cta": "Clear call-to-action (CTA)"
}

Do not explain how you created the content.
Return only the final website copy sections.
"""

EBOOK_CONTENT_TEMPLATE = """
Write a chapter for an e-book.

Chapter title: "{chapter_title}"
Genre / subject: {subject}
Overall e-book theme: {ebook_theme}
Target audience: {target_audience}
Tone: {tone}
Desired length: approximately {word_count} words

Return ONLY valid JSON with this exact schema:
{
  "chapter_title": "Chapter title",
  "content": "Full chapter content with markdown headings, sections, examples, and exercises"
}

Do not explain how you created the content.
Return only the final e-book chapter.
"""

SEO_ARTICLE_TEMPLATE = """
Write an SEO-friendly article on the topic: "{topic}"

Primary keyword: {primary_keyword}
Secondary keywords: {keywords}
Target audience: {target_audience}
Tone: {tone}
Desired length: approximately {word_count} words
SEO title (meta title, max 60 characters): {seo_title}

Return ONLY valid JSON with this exact schema:
{
  "title": "Compelling H1 title with primary keyword",
  "content": "Full article content with H2/H3 headings, body text, internal linking suggestions, conclusion, and meta description"
}

Do not explain how you created the content.
Return only the final SEO article.
"""
