import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from services.prompts import SYSTEM_PROMPT
from services.llm_service import get_llm, get_embeddings
from services.document_service import get_text_splitter


from views.home_view import render_home_page
from views.documents_view import render_documents_page,clear_saved_pdfs_on_startup
from views.chat_view import render_chat_page
from views.summary_view import render_summary_page
from views.quiz_view import render_quiz_page


load_dotenv()





st.set_page_config(
    page_title="AI Study Mate",
    page_icon="🎓",
    layout="wide"
)

clear_saved_pdfs_on_startup()

st.title("🎓 AI Study Mate")
st.caption("Your personal AI-powered study assistant")

if "page" not in st.session_state:
    st.session_state.page = "Home"



if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False
    
if "pdf_names" not in st.session_state:
    st.session_state.pdf_names = []

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


with st.sidebar:
    st.title("📚 AI Study Mate")
    st.caption("Your personal study workspace")
    st.divider()

    st.markdown("#### WORKSPACE")

    if st.button("🏠  Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("💬  Ask AI", use_container_width=True):
        st.session_state.page = "Ask AI"
        st.rerun()

    if st.button("📝  Summarize", use_container_width=True):
        st.session_state.page = "Summarize"
        st.rerun()

    if st.button("🎯  Practice Quiz", use_container_width=True):
        st.session_state.page = "Practice Quiz"
        st.rerun()

    if st.button("📚  My Documents", use_container_width=True):
        st.session_state.page = "My Documents"
        st.rerun()

    # Show New Chat only on the Ask AI page
    if st.session_state.page == "Ask AI":
        st.divider()

        if st.button(
            "＋ New Chat",
            use_container_width=True,
            disabled=st.session_state.is_generating
        ):
            st.session_state.messages = []
            st.session_state.pending_question = None
            st.rerun()



if st.session_state.page == "Home":
    render_home_page()
    

llm = get_llm()
embeddings = get_embeddings()

text_splitter = get_text_splitter()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",SYSTEM_PROMPT),
        ("human","{input}")
    ]
)


# --------------------------------------------------
# MY DOCUMENTS: PDF UPLOAD AND DOCUMENT CARDS
# --------------------------------------------------

if st.session_state.page == "My Documents":
    render_documents_page(text_splitter, embeddings)

# --------------------------------------------------
# ASK AI: EXISTING RAG CHAT
# --------------------------------------------------

if st.session_state.page == "Ask AI":
    document_chain = None

    if "vectorstore" in st.session_state:
        document_chain = create_stuff_documents_chain(
            llm,
            prompt
        )

    render_chat_page(document_chain)
    
if st.session_state.page == "Summarize":
    render_summary_page(llm)

                

if st.session_state.page == "Practice Quiz":
    render_quiz_page(llm)

    

    