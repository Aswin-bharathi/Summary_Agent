import streamlit as st
import google.generativeai as genai
import PyPDF2
from docx import Document
import os
from io import BytesIO

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

st.set_page_config(page_title="📚 AI Notes Summarizer", page_icon="📖", layout="wide")

st.title("📚 AI Class Notes Summarizer")
st.markdown("**Summarize your class notes from PDF, DOCX, or TXT files using Gemini API 🚀**")

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading TXT: {e}")
        return ""

def extract_text_from_docx(file):
    try:
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""

def summarize_text(text, length="short"):
    prompt = f"Summarize the following class notes in a {length} form:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

uploaded_file = st.file_uploader("📥 Upload your class notes", type=["pdf", "txt", "docx"])

if uploaded_file is not None:
    file_size = uploaded_file.size / (1024 * 1024) 

    if file_size > 10:
        st.error("❌ File too large. Max supported size is 10MB.")
        st.stop()

    st.success(f"✅ Uploaded: {uploaded_file.name} ({file_size:.2f} MB)")

    file_type = uploaded_file.type
    if file_type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == "text/plain":
        text = extract_text_from_txt(uploaded_file)
    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("❌ Unsupported file format.")
        st.stop()

    if text:
        st.write(f"📊 **Word count:** `{len(text.split())}`")

        with st.expander("📜 View Original Text"):
            st.text_area("Full Text", text, height=300)

        summary_length = st.radio("📏 Choose summary type:", ["short", "medium", "detailed"])

        if st.button("✨ Summarize Now"):
            with st.spinner("Summarizing your notes using Gemini API..."):
                summary = summarize_text(text, summary_length)

            st.subheader("📖 AI Summary")
            st.write(summary)

            clean_summary = "\n\n".join([line.strip() for line in summary.splitlines() if line.strip()])
            file_content = "AI Generated Summary\n\n" + clean_summary

            st.download_button(
            label="📥 Download Summary as .txt",
            data=BytesIO(file_content.encode('utf-8')),
            file_name="AI_Summary.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ No readable text found in the file.")

else:
    st.info("📌 Upload a PDF, TXT, or DOCX file to begin summarizing.")


st.markdown("---")
st.markdown("💡 *Built with Gemini API & Streamlit | By **Asanth Bro** 🚀*")

st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("🌗 You can switch Light/Dark mode from ⚙️ Streamlit settings in the top-right menu.")

