import streamlit as st
import os
from llama_parse import LlamaParse


# Set API Key for LlamaParse
os.environ["LLAMA_CLOUD_API_KEY"] = "your_api_key"  # 🔴 Replace with your actual API key

# Streamlit Page Config
st.set_page_config(page_title="Document Extractor", layout="wide")
st.title("📄 Document Text Extractor")

st.write("Upload a document and extract its text.")

# File Uploader
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    # Save Uploaded File Temporarily
    temp_file_path = f"temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.write("File uploaded successfully!")

    # Extract text using LlamaParse
    with st.spinner("Extracting text... ⏳"):
        try:
            parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="markdown")
            documents = parser.load_data(temp_file_path)
            
            if not documents:
                st.error("🚨 LlamaParse returned an empty response!")
            else:
                extracted_text = "\n\n".join([doc.text for doc in documents])
                st.text_area("📜 Extracted Text", extracted_text, height=300)
        except Exception as e:
            st.error(f"⚠️ Error extracting text: {str(e)}")

    # Save Extracted Content to Markdown
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

    # Cleanup Temporary File
    os.remove(temp_file_path)
