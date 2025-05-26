import streamlit as st
import openai
import base64

# ---- Configuration ----
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store securely in Streamlit secrets

# ---- App Title ----
st.set_page_config(page_title="GPT-4V OCR & Markdown Extractor", layout="wide")
st.title("🧠 GPT-4 Vision: OCR and Markdown Formatter")
st.markdown("""
Upload an image with text or tables. GPT-4 Vision will extract and structure the content into clear, formatted **Markdown**, including tables if present.

✅ No local installs required.  
✅ Ideal for scanned documents, forms, and structured content.
""")

# ---- Upload Column Layout ----
col1, col2 = st.columns([1.5, 1])

with col2:
    uploaded_file = st.file_uploader("📤 Upload Image (JPG or PNG)", type=["jpg", "jpeg", "png"], help="Upload a clear image with readable text or tables.")

if uploaded_file:
    image_bytes = uploaded_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    with col1:
        st.image(image_bytes, caption="📷 Uploaded Image", use_container_width=True)

    with st.spinner("🧠 Analyzing image using GPT-4 Vision..."):
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all readable text from the image and format it as clear, structured Markdown. Use tables, lists, and headings where appropriate."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]
                }
            ],
            max_tokens=2000
        )

    markdown_output = response.choices[0].message.content

    # ---- Result Section ----
    st.subheader("📝 Extracted Markdown")
    st.markdown(markdown_output)
else:
    st.info("👈 Please upload an image to begin OCR and formatting.")
