import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except PyPDF2.errors.PdfReadError:
        st.error("❌ Error reading the PDF file. It might be corrupted or incomplete.")
        return ""
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
        return ""

def summarize_text(text, length="short"):
    prompt = f"Summarize the following class notes in a {length} form:\n{text}"
    response = model.generate_content(prompt)
    return response.text

st.title("📚 AI Class Notes Summarizer (Gemini API)")

uploaded_file = st.file_uploader("Upload your class notes (PDF format only)", type=["pdf"])

if uploaded_file is not None:
   
    if uploaded_file.type == "application/pdf":
        st.success("✅ File uploaded successfully!")
     
        text = extract_text_from_pdf(uploaded_file)
        
        if text:
            st.write("📏 Choose your summary length:")
            summary_length = st.radio("Select one:", ["short", "medium", "detailed"])

            if st.button("✨ Summarize Now"):
                with st.spinner("Summarizing your notes..."):
                    summary = summarize_text(text, summary_length)
                st.subheader("📖 Summary:")
                st.write(summary)
        else:
            st.warning("⚠️ No readable text found in the PDF.")
    else:
        st.error("❌ Please upload a valid PDF file.")

