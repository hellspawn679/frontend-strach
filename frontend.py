import streamlit as st
import docx2txt
import pdfplumber
import requests
import json 
import requests
import json

st.set_page_config(
    page_title="multi-page app",

)
st.title("main page")
st.sidebar.success("select a page above.")



def process_document_file(docx_file):
    """
    Process the uploaded document file and extract the text content.

    Parameters:
    docx_file (FileUploader): The uploaded document file.

    Returns:
    dict: A dictionary containing the filename, filetype, filesize, and extracted text content.
    """
    if docx_file is not None:
        if docx_file.type == "text/plain":
            # Read as string (decode bytes to string)
            raw_text = str(docx_file.read(), "utf-8")
        elif docx_file.type == "application/pdf":
            try:
                with pdfplumber.open(docx_file) as pdf:
                    raw_text = ""
                    for i in range(len(pdf.pages)):
                       pages = pdf.pages[i]
                       raw_text += pages.extract_text()
            except:
                raw_text = ""
                st.write("None text found")
        else:
            raw_text = docx2txt.process(docx_file)
        file_details = {
            "filename": docx_file.name,
            "filetype": docx_file.type,
            "filesize": docx_file.size,
            "data": raw_text
        }
        return file_details



st.subheader("DocumentFiles")
docx_file = st.file_uploader("Upload Document", type=["pdf","docx","txt"])
file_data=process_document_file(docx_file)

if st.button('Send to FastAPI'):
    st.write(file_data['data'])
    if file_data is not None:
        try:
            response = requests.post('http://127.0.0.1:8000/upload/', json=file_data)
            
        except Exception as e:
            st.write("Error:", e)
    else:
        st.write("No file uploaded or unsupported file type")
            
