import os
import streamlit as st
from llama_parse import LlamaParse

# Load API Key from environment variables
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY", "")

# Display API Key Status
if not LLAMA_API_KEY:
    st.error("⚠️ Missing API Key! Set 'LLAMA_CLOUD_API_KEY' as an environment variable.")
else:
    st.success("✅ API Key Loaded Successfully!")

# Initialize LlamaParse if API key is present
parser = None
if LLAMA_API_KEY:
    parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="markdown")

# File Uploader
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

# Initialize extracted_text to prevent undefined variable errors
extracted_text = ""

if uploaded_file is not None:
    temp_file_path = f"temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.write("📂 File uploaded successfully!")

    if parser:
        with st.spinner("Extracting text... ⏳"):
            try:
                documents = parser.load_data(temp_file_path)
                if documents:
                    extracted_text = "\n\n".join([doc.text for doc in documents])
                    st.success("✅ Text Extracted Successfully!")
                else:
                    st.error("🚨 No text extracted. The document may be empty or unsupported.")
            except Exception as e:
                st.error(f"⚠️ Error extracting text: {str(e)}")
    else:
        st.error("🚨 LlamaParse is not initialized. Check your API key.")

    # Ensure extracted_text is always defined
    if extracted_text:
        st.text_area("📜 Extracted Text", extracted_text, height=300)

        # Save Extracted Text to Markdown File
        md_file_path = "document.md"
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        # Provide Download Option
        with open(md_file_path, "rb") as f:
            st.download_button(
                label="📥 Download Extracted Text",
                data=f,
                file_name="extracted_text.md",
                mime="text/markdown",
            )
