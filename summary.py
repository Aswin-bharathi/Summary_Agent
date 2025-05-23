import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


# Function to extract text from PDF using PyPDF2 safely
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

# Optional: you can switch to this if PyPDF2 keeps failing
# import pdfplumber
# def extract_text_from_pdf(pdf_file):
#     text = ""
#     with pdfplumber.open(pdf_file) as pdf:
#         for page in pdf.pages:
#             content = page.extract_text()
#             if content:
#                 text += content
#     return text

# Function to summarize text using Gemini API
def summarize_text(text, length="short"):
    prompt = f"Summarize the following class notes in a {length} form:\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Streamlit App Interface
st.title("📚 AI Class Notes Summarizer (Gemini API)")

# File uploader
uploaded_file = st.file_uploader("Upload your class notes (PDF format only)", type=["pdf"])

if uploaded_file is not None:
    # Check file type
    if uploaded_file.type == "application/pdf":
        st.success("✅ File uploaded successfully!")
        
        # Extract text from PDF
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

