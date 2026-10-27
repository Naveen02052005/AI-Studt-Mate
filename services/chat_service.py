
import os


def get_relevant_documents(retriever, question):
    return retriever.invoke(question)


def prepare_sources(retrieved_docs):
    sources = []

    for doc in retrieved_docs:
        source_file = doc.metadata.get(
            "source_file",
            doc.metadata.get("source", "Unknown PDF")
        )

        try:
            page_number = int(doc.metadata.get("page", 0)) + 1
        except (TypeError, ValueError):
            page_number = 1

        source = {
            "file": os.path.basename(str(source_file)),
            "page": page_number,
            "excerpt": doc.page_content[:600]
        }

        if source not in sources:
            sources.append(source)

    return sources


def generate_chat_answer(document_chain, question, retrieved_docs):
    return document_chain.stream({
        "input": question,
        "context": retrieved_docs
    })
