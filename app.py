"""
AI Agent Assignment – Streamlit Web Application
===============================================

A professional, multi-agent AI workspace that lets users switch between
three specialised agents:

1. **Content Writing Agent** – blogs, website copy, e-book content, SEO articles
2. **Copywriting & Ads Agent** – Facebook / Google / LinkedIn ads, product
    descriptions, email copy, CTA variations
3. **Video Production Agent** – scripts, storyboards, shot lists, voice-over
    scripts, social media video concepts

Features
--------
- Sidebar agent selector with demo-mode toggle
- Agent-specific input forms
- Clean markdown output with copy-to-clipboard
- Download results as .md files
- Error handling for missing API keys and API failures
- Predefined demo outputs for offline / interview demonstration

Run with:  streamlit run app.py
"""

import os
import sys
import logging
from datetime import datetime

import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.content_agent import ContentAgent
from agents.copywriting_agent import CopywritingAgent
from agents.video_agent import VideoAgent

logger = logging.getLogger(__name__)

AGENTS = {
    "content": ("Content Writing Agent", "📝"),
    "copywriting": ("Copywriting & Ads Agent", "✍️"),
    "video": ("Video Production Agent", "🎥"),
}

DEMO_VARIANTS = {0: "Demo Output 1", 1: "Demo Output 2", 2: "Demo Output 3"}

OPENROUTER_MODEL_OPTIONS = [
    "nvidia/nemotron-3.5-lightning:free",
]

DEFAULT_OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")


def get_openrouter_client(model_name: str = DEFAULT_OPENROUTER_MODEL):
    """Create and cache an OpenRouterClient (or None if unavailable)."""
    cache_key = f"openrouter_client_{model_name}"
    if cache_key not in st.session_state:
        try:
            from utils.openrouter_client import OpenRouterClient
            st.session_state[cache_key] = OpenRouterClient(model=model_name)
        except Exception as exc:
            st.error(f"Failed to initialise OpenRouter client: {exc}")
            st.session_state[cache_key] = None
    return st.session_state[cache_key]


@st.cache_resource
def get_content_agent(model_name: str = DEFAULT_OPENROUTER_MODEL):
    return ContentAgent(get_openrouter_client(model_name))


@st.cache_resource
def get_copywriting_agent(model_name: str = DEFAULT_OPENROUTER_MODEL):
    return CopywritingAgent(get_openrouter_client(model_name))


@st.cache_resource
def get_video_agent(model_name: str = DEFAULT_OPENROUTER_MODEL):
    return VideoAgent(get_openrouter_client(model_name))


def download_button(content: str, filename: str, label: str = "Download"):
    """Render a download button using Streamlit's built-in method."""
    st.download_button(
        label=f"📥 {label}",
        data=content,
        file_name=filename,
        mime="text/markdown",
    )


def copy_output(content: str, key: str):
    """Provide copy-to-clipboard via a code block."""
    with st.expander("📋 Copy to clipboard"):
        st.code(content, language=None)


def render_sidebar():
    """Build the left sidebar with agent selection and mode toggle."""
    st.sidebar.title("AI Agent Workspace")

    # AI Model info
    st.sidebar.markdown("**AI Model:**")
    st.sidebar.code("NVIDIA Nemotron 3.5 Lightning", language=None)
    st.sidebar.markdown("**Provider:**")
    st.sidebar.code("OpenRouter", language=None)
    st.sidebar.markdown("---")

    # Mode toggle (Demo vs. OpenRouter)
    demo_mode = st.sidebar.radio(
        "Mode",
        options=["Demo Mode", "OpenRouter Mode"],
        index=0,
        help="Demo Mode uses pre-written samples. OpenRouter Mode requires a valid OPENROUTER_API_KEY.",
    )

    st.sidebar.markdown("---")

    # Test OpenRouter Connection button
    if st.sidebar.button("🔍 Test OpenRouter Connection", use_container_width=True):
        test_client = get_openrouter_client(DEFAULT_OPENROUTER_MODEL)
        if test_client is None:
            st.sidebar.error(
                "❌ **OpenRouter client failed to initialise.**\n\n"
                "Ensure OPENROUTER_API_KEY is set in .env and the app has been restarted."
            )
        else:
            ok, msg = test_client.check_connection()
            if ok:
                st.sidebar.success(f"✅ {msg}")
            else:
                st.sidebar.error(f"❌ {msg}")

    st.sidebar.markdown("---")

    # Agent selector
    selected_agent = st.sidebar.radio(
        "Select Agent",
        options=list(AGENTS.keys()),
        format_func=lambda key: f"{AGENTS[key][1]} {AGENTS[key][0]}",
    )

    # Demo variant selector (only visible in Demo Mode)
    if demo_mode == "Demo Mode":
        st.sidebar.markdown("---")
        demo_variant = st.sidebar.selectbox(
            "Demo Sample",
            options=list(DEMO_VARIANTS.keys()),
            format_func=lambda k: DEMO_VARIANTS[k],
        )
    else:
        demo_variant = 0

    return selected_agent, demo_mode == "Demo Mode", demo_variant


def render_content_agent_inputs(agent: ContentAgent, demo_mode: bool, demo_variant: int):
    """Render the input form and handle generation for the Content Agent."""
    st.header("📝 Content Writing Agent")
    st.caption("Generate blogs, website content, e-book chapters, and SEO articles.")

    content_types = agent.get_content_types()
    content_type = st.selectbox("Content Type", options=list(content_types.keys()),
                                format_func=lambda k: content_types[k])

    topic = st.text_input("Topic", placeholder="e.g. How to Build a Morning Routine")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Busy professionals")
    tone = st.selectbox("Tone", options=["Professional", "Casual", "Inspirational", "Urgent", "Conversational"])
    word_count = st.slider("Approximate Word Count", 300, 5000, 1500, step=100)
    keywords = st.text_input("Keywords (comma separated)", placeholder="e.g. morning routine, productivity, wellness")
    extra_context = st.text_area("Additional Context (optional)",
                                 placeholder="e.g. Tone: conversational; include examples")

    if st.button("Generate Content", type="primary", use_container_width=True):
        if not topic.strip():
            st.error("Please enter a topic.")
            return
        _run_generation(
            agent=agent,
            content_type=content_type,
            topic=topic,
            target_audience=target_audience,
            tone=tone,
            word_count=word_count,
            keywords=keywords,
            extra_context=extra_context,
            demo_mode=demo_mode,
            demo_variant=demo_variant,
            output_label=f"content_{content_type}",
        )


def render_copywriting_agent_inputs(agent: CopywritingAgent, demo_mode: bool, demo_variant: int):
    """Render the input form and handle generation for the Copywriting Agent."""
    st.header("✍️ Copywriting & Ads Agent")
    st.caption("Generate ads, product descriptions, email copy, and CTAs.")

    ad_types = agent.get_ad_types()
    ad_type = st.selectbox("Content Type", options=list(ad_types.keys()),
                           format_func=lambda k: ad_types[k])

    product = st.text_input("Product / Service", placeholder="e.g. FitTrack Pro fitness app")
    platform = st.selectbox("Platform", options=["Facebook", "Google Ads", "LinkedIn", "Email", "Website"])
    target_audience = st.text_input("Target Audience", placeholder="e.g. Fitness enthusiasts 25-45")
    campaign_objective = st.selectbox("Campaign Objective", options=[
        "Brand Awareness", "Lead Generation", "Sales Conversion", "Engagement", "Traffic"
    ])
    tone = st.selectbox("Tone", options=["Professional", "Playful", "Inspirational",
                                         "Urgent", "Trustworthy", "Conversational"])
    key_benefit = st.text_input("Key Benefit / Value Proposition", placeholder="e.g. Saves 10 hours per week")
    extra_context = st.text_area("Additional Context (optional)",
                                 placeholder="e.g. Key benefits: saves time, increases energy; URL: https://example.com")

    if st.button("Generate Copy", type="primary", use_container_width=True):
        if not product.strip():
            st.error("Please enter a product or service.")
            return
        _run_generation(
            agent=agent,
            ad_type=ad_type,
            product=product,
            platform=platform,
            target_audience=target_audience,
            campaign_objective=campaign_objective,
            tone=tone,
            key_benefit=key_benefit,
            extra_context=extra_context,
            demo_mode=demo_mode,
            demo_variant=demo_variant,
            output_label=f"copy_{ad_type}",
        )


def render_video_agent_inputs(agent: VideoAgent, demo_mode: bool, demo_variant: int):
    """Render the input form and handle generation for the Video Agent."""
    st.header("🎥 Video Production Agent")
    st.caption("Generate scripts, storyboards, shot lists, and social media concepts.")

    video_types = agent.get_video_types()
    video_type = st.selectbox("Content Type", options=list(video_types.keys()),
                              format_func=lambda k: video_types[k])

    topic = st.text_input("Video Topic", placeholder="e.g. The Morning Stack – Product Demo")
    platform = st.selectbox("Platform", options=["YouTube", "Instagram Reels", "YouTube Shorts", "LinkedIn", "TikTok"])
    duration = st.text_input("Target Duration", placeholder="e.g. 60 seconds", value="60 seconds")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Tech-savvy consumers")
    video_style = st.selectbox("Video Style", options=["Professional", "Casual", "Dramatic",
                                                       "Inspirational", "Humorous", "Cinematic"])
    cta = st.text_input("Call to Action (CTA)", placeholder="e.g. Subscribe now, Download free trial")
    extra_context = st.text_area("Additional Context (optional)",
                                 placeholder="e.g. Scenes: 5, Camera: iPhone 15 Pro, Lighting setup details...")

    if st.button("Generate Video Content", type="primary", use_container_width=True):
        if not topic.strip():
            st.error("Please enter a video topic.")
            return
        _run_generation(
            agent=agent,
            video_type=video_type,
            topic=topic,
            platform=platform,
            duration=duration,
            target_audience=target_audience,
            tone=video_style,
            cta=cta,
            extra_context=extra_context,
            demo_mode=demo_mode,
            demo_variant=demo_variant,
            output_label=f"video_{video_type}",
        )


def _run_generation(agent, demo_mode: bool, demo_variant: int,
                    output_label: str, **kwargs):
    """
    Call the correct agent method, display the result, and provide
    copy / download actions.
    """
    placeholder = st.empty()

    if not demo_mode:
        client = get_openrouter_client(DEFAULT_OPENROUTER_MODEL)
        if client is None:
            st.error(
                "🖥️ **OpenRouter is not available.**\n\n"
                "To use OpenRouter Mode:\n"
                "1. Get an OpenRouter API key from https://openrouter.ai/keys\n"
                "2. Add OPENROUTER_API_KEY to your .env file\n"
                "3. Restart the app\n\n"
                "Alternatively, switch to **Demo Mode** in the sidebar to "
                "test all features without an API key."
            )
            return

        ok, msg = client.check_connection()
        if not ok:
            st.error(f"❌ **OpenRouter connection failed:** {msg}")
            return

    try:
        with placeholder:
            if "Generating" not in st.session_state:
                st.markdown("*Generating…*")

            result = agent.generate(demo_mode=demo_mode, demo_variant=demo_variant, **kwargs)

            if isinstance(result, str) and result.startswith("Error:"):
                raise RuntimeError(result)

        placeholder.empty()
        _render_result(result, output_label, demo_mode)

    except RuntimeError as exc:
        placeholder.empty()
        st.error(f"❌ **Error:** {exc}")
    except Exception as exc:
        placeholder.empty()
        st.error(f"❌ **Unexpected error:** {exc}")
        logger.exception("Generation failed")


def _render_result(content: str, output_label: str, demo_mode: bool):
    """
    Display the generated content in a clean output section with
    copy and download controls.
    """
    st.markdown("---")
    st.subheader("📋 Generated Output")

    if demo_mode:
        st.info("📋 **Demo Mode — Predefined Sample Output** — This output is a pre-written sample and was **not** generated by OpenRouter. Switch to 'OpenRouter Mode' in the sidebar for real AI generation.")

    st.markdown(content)

    col1, col2 = st.columns([1, 1])
    with col1:
        copy_output(content, key=output_label)
    with col2:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_label}_{timestamp}.md"
        download_button(content, filename=filename, label="Download as .md")

    st.session_state["last_output"] = content
    st.session_state["last_output_label"] = output_label


def main():
    """Entry point for the Streamlit application."""

    st.set_page_config(
        page_title="AI Agent Assignment",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    selected_agent_key, demo_mode, demo_variant = render_sidebar()

    st.title("🤖 AI Agent Assignment")
    st.caption(
        "Three specialised AI agents for content writing, copywriting, "
        "and video production. Powered by **OpenRouter** with a "
        "built-in demo mode for offline use."
    )

    if demo_mode:
        st.warning(
            "📋 **Demo Mode is active.** Outputs are pre-written samples. "
            "Switch to 'OpenRouter Mode' in the sidebar for real AI generation.",
            icon="📋",
        )

    if selected_agent_key == "content":
        agent = get_content_agent(DEFAULT_OPENROUTER_MODEL)
        render_content_agent_inputs(agent, demo_mode, demo_variant)

    elif selected_agent_key == "copywriting":
        agent = get_copywriting_agent(DEFAULT_OPENROUTER_MODEL)
        render_copywriting_agent_inputs(agent, demo_mode, demo_variant)

    elif selected_agent_key == "video":
        agent = get_video_agent(DEFAULT_OPENROUTER_MODEL)
        render_video_agent_inputs(agent, demo_mode, demo_variant)

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #6474a5; font-size: 12px;">
        AI Agent Assignment • Built with <a href="https://streamlit.io/" target="_blank">Streamlit</a> 
        and <a href="https://openrouter.ai" target="_blank">OpenRouter</a> • 
        All configuration is loaded from environment variables and never stored in code.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
