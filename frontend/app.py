"""Minimal Streamlit UI for the AI Agentic Marketing Engine."""

import json
import requests
import streamlit as st

API_BASE = st.secrets.get("API_BASE", "http://localhost:8001/api/v1")

st.set_page_config(page_title="Codagem Engine", layout="wide")
st.title("Codagem — AI Agentic Marketing Engine")

# ── Sidebar ─────────────────────────────────────────
with st.sidebar:
    st.header("System")
    if st.button("Health Check"):
        try:
            r = requests.get(f"{API_BASE.replace('/api/v1','')}/health", timeout=5)
            st.json(r.json())
        except Exception as e:
            st.error(f"API unavailable: {e}")

    if st.button("View Agents"):
        try:
            r = requests.get(f"{API_BASE.replace('/api/v1','')}/agents", timeout=5)
            st.json(r.json())
        except Exception as e:
            st.error(f"API unavailable: {e}")

    if st.button("View Workflows"):
        try:
            r = requests.get(f"{API_BASE.replace('/api/v1','')}/workflows", timeout=5)
            st.json(r.json())
        except Exception as e:
            st.error(f"API unavailable: {e}")

# ── Main input form ─────────────────────────────────
st.subheader("Generate Instagram Campaign")

col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("Product Name", placeholder="e.g. Premium Wireless Earbuds")
    affiliate_link = st.text_input("Affiliate Link", placeholder="https://your-link.com/product")
    niche = st.text_input("Niche", placeholder="e.g. Tech, Fitness, Beauty")
with col2:
    audience = st.text_input("Target Audience", placeholder="e.g. Young professionals 25-35")
    objective = st.selectbox("Objective", ["conversions", "awareness", "engagement", "leads"])
    tone = st.selectbox("Tone", ["persuasive", "luxury", "casual", "urgent", "inspirational", "educational"])

if st.button("Generate Campaign", type="primary", use_container_width=True):
    if not all([product_name, affiliate_link, niche, audience]):
        st.error("All fields are required.")
    else:
        with st.spinner("Running multi-agent workflow... This may take 1-3 minutes."):
            try:
                payload = {
                    "product_name": product_name,
                    "affiliate_link": affiliate_link,
                    "niche": niche,
                    "audience": audience,
                    "objective": objective,
                    "tone": tone,
                }
                r = requests.post(
                    f"{API_BASE}/generate-campaign",
                    json=payload,
                    timeout=600,
                )
                if r.status_code == 200:
                    result = r.json()
                    st.session_state["campaign"] = result
                    st.success("Campaign generated!")
                else:
                    st.error(f"Generation failed: {r.text}")
            except requests.exceptions.ReadTimeout:
                st.error("Request timed out. The workflow may still be running on the server.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the API server. Make sure the backend is running on port 8001.")
            except Exception as e:
                st.error(f"Error: {e}")

# ── Display results ─────────────────────────────────
campaign = st.session_state.get("campaign")
if campaign:
    st.divider()
    st.subheader("Campaign Package")

    # Quality score
    quality = campaign.get("quality", {})
    score = quality.get("score", 0)
    st.metric("Quality Score", f"{score}/10")

    content = campaign.get("content", {})
    meta = campaign.get("metadata", {})

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Caption & CTA", "Carousel", "Image", "Hashtags", "Metadata", "JSON Output"]
    )

    with tab1:
        st.markdown("### Headline / Hook")
        st.write(content.get("headline", ""))
        st.markdown("### Caption")
        st.write(content.get("caption", ""))
        st.markdown("### CTA")
        st.info(content.get("cta", ""))

    with tab2:
        slides = content.get("carousel_slides", [])
        if isinstance(slides, list):
            for slide in slides:
                if isinstance(slide, dict):
                    st.markdown(f"**Slide {slide.get('slide_number', '?')}: {slide.get('type', '')}**")
                    st.write(f"**{slide.get('headline', '')}**")
                    st.write(slide.get("body", ""))
                    if slide.get("visual_direction"):
                        st.caption(f"Visual: {slide['visual_direction']}")
                    st.divider()
                else:
                    st.write(slides)

    with tab3:
        st.markdown("### Image Prompt")
        st.write(content.get("image_prompt", ""))
        img_path = content.get("generated_image", "")
        if img_path:
            st.markdown("### Generated Image")
            try:
                st.image(img_path)
            except Exception:
                st.info(f"Image saved at: {img_path}")

    with tab4:
        tags = content.get("hashtags", [])
        if tags:
            st.markdown("### Hashtags")
            st.write(" ".join(f"#{t.lstrip('#')}" for t in tags))

    with tab5:
        st.markdown("### Strategy")
        st.write(meta.get("strategy", ""))
        st.markdown("### Persona")
        st.write(meta.get("persona", ""))
        st.markdown("### Pain Points")
        for p in meta.get("pain_points", []):
            st.write(f"- {p}")
        st.markdown("### Benefits")
        for b in meta.get("benefits", []):
            st.write(f"- {b}")

    with tab6:
        st.json(campaign)
