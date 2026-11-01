"""
GemmaFlow - Multimodal Open-Source Assistant powered by Gemma 4
Built for Hacktoberfest Hack Day Ahmedabad x NavraCommunity
"""

import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="GemmaFlow - Open-Source Multimodal AI",
    page_icon="🌟",
    layout="wide"
)

st.title("🌟 GemmaFlow: Multimodal AI Assistant")
st.markdown("Powered by **Gemma 4** open-weights model via Google Gemini API.")

# Sidebar for Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
    model_name = st.selectbox(
        "Model Selection",
       options=["gemma-4-26b-a4b-it", "gemma-3-27b-it", "gemini-2.5-flash"],
        index=0,
        help="Gemma 4 provides lightweight multimodal reasoning."
    )
    st.markdown("---")
    st.markdown("### 🏆 Hacktoberfest Tracks")
    st.markdown("- **Best Use of Gemma 4**")
    st.markdown("- **Best Open-Source AI Project**")

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Input Context")
    uploaded_image = st.file_uploader(
        "Upload an image (Diagram, UI mockup, or Error Screenshot)",
        type=["png", "jpg", "jpeg", "webp"]
    )
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Artifact", use_column_width=True)

    prompt = st.text_area(
        "Prompt / Instructions",
        placeholder="e.g., Explain this architecture diagram, extract API endpoints, or debug this error trace...",
        height=140
    )
    analyze_btn = st.button("🚀 Analyze with Gemma 4", type="primary")

with col2:
    st.subheader("💡 Analysis & Insights")
    if analyze_btn:
        if not api_key:
            st.error("Please provide a Gemini API Key in the sidebar.")
        elif not prompt and not uploaded_image:
            st.warning("Please provide a prompt or upload an image.")
        else:
            with st.spinner("Processing with Gemma 4..."):
                try:
                    client = genai.Client(api_key=api_key)
                    contents = []
                    if uploaded_image:
                        contents.append(image)
                    if prompt:
                        contents.append(prompt)

                    response = client.models.generate_content(
                        model=model_name,
                        contents=contents
                    )
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Inference Error: {str(e)}")
