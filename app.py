import streamlit as st
from ollama import Client  # <-- Change this line
from PIL import Image

st.set_page_config(page_title="Gemma3 OCR with Ollama", layout="wide")

# Sidebar Help/Info
st.sidebar.title("ℹ️ How to Use")
st.sidebar.markdown(
    """
    1. Upload an image (JPG/PNG) on the right panel.  
    2. Click **Analyze Image** to extract and format text.  
    3. See clean, structured OCR output below the title.  
    4. Supported formats: JPG, PNG.  

    This app uses the powerful **Gemma 3 (12B)** LLM via Ollama to perform OCR **and** 
    format the extracted text in Markdown for easy reading.
    """
)

# Main Title
st.title("🧠 Gemma3 OCR & Markdown Formatter")

# Layout: two columns: left for OCR text, right for upload + image preview
col_text, col_upload = st.columns([3,1])

with col_upload:
    uploaded_file = st.file_uploader("📤 Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Ollama client init (once)
@st.cache_resource
def get_ollama_client():
    return Client(host='http://localhost:11434')  # Default Ollama port

ollama = get_ollama_client()

# OCR result placeholder
if 'ocr_result' not in st.session_state:
    st.session_state['ocr_result'] = ""

# OCR interaction logic
if uploaded_file:
    # Show uploaded image
    with col_upload:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    # Automatically process the image when uploaded
    if st.session_state.get('last_uploaded_filename') != uploaded_file.name:
        with st.spinner("Processing image with Gemma 3..."):
            try:
                response = ollama.chat(
                    model='gemma3:12b',
                    messages=[{
                        'role': 'user',
                        'content': (
                            "Analyze the text in the provided image. Extract all readable content "
                            "and present it in a structured Markdown format that is clear, concise, "
                            "and well-organized. Ensure proper formatting (e.g., headings, lists, or "
                            "code blocks) as necessary to represent the content effectively."
                        ),
                        'images': [uploaded_file.getvalue()]
                    }]
                )
                st.session_state['ocr_result'] = response.message.content
                st.session_state['last_uploaded_filename'] = uploaded_file.name
            except Exception as e:
                st.error(f"⚠️ Error during analysis: {e}")

# Display extracted OCR result just below the title in the left column
with col_text:
    st.subheader("📝 Extracted & Formatted Text")
    if st.session_state['ocr_result']:
        st.markdown(st.session_state['ocr_result'], unsafe_allow_html=True)
    else:
        st.info("Upload an image and click 'Analyze Image' to see extracted text here.")

# Footer / additional tips
st.markdown("---")
st.markdown(
    """
    *Tip: For best results, upload clear images with good contrast and legible text.*  
    *This app relies on Ollama's Gemma 3 LLM for OCR and formatting — local Ollama setup required.*
    """
)
