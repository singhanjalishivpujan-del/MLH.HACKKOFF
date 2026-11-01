import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GemmaFlow AI Assistant",
    page_icon="🌟",
    layout="wide"
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🌟 GemmaFlow")

    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password"
    )

    model_name = st.selectbox(
        "Select AI Model",
        [
            "gemini-2.5-flash",
            "gemma-3-27b-it"
        ]
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "💬 AI Chat",
            "🖼️ Image Analysis",
            "✍️ Writing Assistant",
            "💻 Coding Assistant"
        ]
    )

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Google Gemini API")

# AI function
def generate_response(prompt, image=None):

    if not api_key:
        return "Please enter your Gemini API Key in the sidebar."

    try:
        client = genai.Client(api_key=api_key)

        contents = []

        if image:
            contents.append(image)

        contents.append(prompt)

        response = client.models.generate_content(
            model=model_name,
            contents=contents
        )

        return response.text or "No response generated."

    except Exception as e:
        return f"Error: {str(e)}"


# HOME PAGE
if page == "🏠 Home":

    st.title("🌟 Welcome to GemmaFlow")

    st.subheader("Your All-in-One AI Assistant")

    st.write(
        "One platform for learning, coding, writing, "
        "image understanding and everyday tasks."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.info("📚 **Study Assistant**\n\nUnderstand topics and learn concepts.")

        st.info("💻 **Coding Assistant**\n\nGenerate and explain programming code.")

        st.info("🖼️ **Image Analysis**\n\nUnderstand images and diagrams.")

    with col2:
        st.info("✍️ **Writing Assistant**\n\nCreate emails, reports and captions.")

        st.info("💬 **AI Chat**\n\nAsk questions and get AI responses.")

        st.info("🚀 **More Features**\n\nNew capabilities coming soon.")

    st.success("Select a feature from the sidebar to get started.")


# AI CHAT
elif page == "💬 AI Chat":

    st.title("💬 AI Chat")

    st.write("Ask anything and chat with your AI assistant.")

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask GemmaFlow anything...")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # Build conversation context
        conversation = ""

        for message in st.session_state.messages[:-1]:
            conversation += (
                f'{message["role"]}: {message["content"]}\n'
            )

        conversation += f"user: {user_input}"

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = generate_response(conversation)

                st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


# IMAGE ANALYSIS
elif page == "🖼️ Image Analysis":

    st.title("🖼️ Image Analysis")

    st.write("Upload an image and ask questions about it.")

    uploaded_image = st.file_uploader(
        "Upload your image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_image:

        image = Image.open(uploaded_image)

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        prompt = st.text_area(
            "What would you like to know about this image?",
            placeholder="Describe this image..."
        )

        if st.button("🔍 Analyze Image", type="primary"):

            with st.spinner("Analyzing image..."):

                answer = generate_response(prompt or "Describe this image.", image)

                st.subheader("AI Analysis")
                st.markdown(answer)


# WRITING ASSISTANT
elif page == "✍️ Writing Assistant":

    st.title("✍️ Writing Assistant")

   task = st.selectbox(
        "Choose your writing task",
        [
            "Write an Email",
            "Create LinkedIn Post",
            "Write an Assignment",
            "Create a Report",
            "Improve Grammar",
            "Summarize Text",
            "Other"
        ]
    )

    user_text = st.text_area(
        "Enter your topic or text",
        height=180
    )

    if st.button("✨ Generate Content", type="primary"):
        if user_text:
            prompt = f"""
            Act as a professional writing assistant.
            Task: {task}
            User input: {user_text}
            Generate clear and useful content.
            """
            with st.spinner("Creating content..."):
                answer = generate_response(prompt)
                st.markdown("### Generated Content")
                st.markdown(answer)
        else:
            st.warning("Please enter some text or a topic.")
