
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource # tells Streamlit to reuse the created resource across reruns rather than recreating it every time.
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite"
    )


@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
