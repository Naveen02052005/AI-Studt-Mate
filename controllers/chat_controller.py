
from services.chat_service import get_relevant_documents,prepare_sources,generate_chat_answer


def prepare_chat_question(question):
    return question.strip()


def process_chat_question(retriever, question):
    retrieved_docs = get_relevant_documents(
        retriever, question
    )
    return retrieved_docs


def get_chat_sources(retrieved_docs):
    return prepare_sources(retrieved_docs)


def stream_chat_answer(document_chain, question, retrieved_docs):
    return generate_chat_answer(
        document_chain, question, retrieved_docs
    )