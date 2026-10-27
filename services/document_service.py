
import os
import tempfile

import pytesseract
import streamlit as st

from pdf2image import convert_from_path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


@st.cache_resource
def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )


def load_pdf_documents(uploaded_pdf):
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(uploaded_pdf.getvalue())
            temp_path = temp_file.name

        loader = PyPDFLoader(temp_path)
        docs = loader.load()

        text_docs = [
            doc for doc in docs
            if doc.page_content.strip()
        ]

        if text_docs:
            docs = text_docs
        else:
            # OCR fallback for scanned PDFs
            images = convert_from_path(
                temp_path,
                poppler_path=r"C:\poppler\Library\bin"
            )

            docs = []

            for page_number, image in enumerate(images):
                extracted_text = pytesseract.image_to_string(image)

                if extracted_text.strip():
                    docs.append(
                        Document(
                            page_content=extracted_text,
                            metadata={"page": page_number}
                        )
                    )

        return docs

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def create_vectorstore(documents, embeddings):
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )
