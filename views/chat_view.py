
import streamlit as st
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

from controllers.chat_controller import (
    prepare_chat_question,
    process_chat_question,
    get_chat_sources,
    stream_chat_answer
)



def render_chat_page(document_chain):
    st.markdown("## 💬 Ask AI")
    st.caption(
        "Your personal study assistant - ask questions about your "
        "uploaded PDFs and get answers with source references."
    )

    st.divider()

    if "vectorstore" not in st.session_state:
        st.info(
            "You haven't processed any PDFs yet. "
            "Open My Documents in the sidebar and upload your "
            "study PDFs first."
        )
        return

    # vectorstore = st.session_state.vectorstore

    # retriever = vectorstore.as_retriever(
    #     search_kwargs={"k": 5}
    # )


# Below retrieval is hybrid retrieval to identify short forms and long forms of entities in the query

    vectorstore = st.session_state.vectorstore

    semantic_retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    study_documents = st.session_state.get(
        "study_documents", []
    )

    keyword_retriever = BM25Retriever.from_documents(
        study_documents
    )
    keyword_retriever.k = 5

    retriever = EnsembleRetriever(
        retrievers=[
            semantic_retriever,
            keyword_retriever
        ],
        weights=[0.5, 0.5]
    )

    if not st.session_state.messages:
        st.markdown("### 👋 What would you like to learn today?")
        st.caption(
            "Ask a question about your uploaded PDFs. "
            "AI Study Mate will answer using your study materials "
            "and provide source references."
        )

    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):
                with st.expander("View source references"):
                    for source in message["sources"]:
                        st.markdown(
                            f"**File:** `{source['file']}`\n\n"
                            f"**Page:** `{source['page']}`"
                        )
                        st.write(source["excerpt"])
                        st.divider()

            if message["role"] == "assistant":
                feedback = st.feedback(
                    "thumbs",
                    key=f"feedback_{i}"
                )

                if feedback is not None:
                    st.session_state.messages[i]["feedback"] = feedback

                    if feedback == 1:
                        st.success(
                            "Thanks! You found this answer helpful."
                        )
                    else:
                        st.info(
                            "Thanks for your feedback. "
                            "We'll work to improve."
                        )

    question = st.chat_input(
        "💬 Ask a question about your study materials...",
        key="study_chat_input",
        disabled=st.session_state.is_generating
    )

    if question and not st.session_state.is_generating:
        question = question.strip()

        if not question:
            st.warning("Please enter a question before processing Enter.")
        else:
            question = prepare_chat_question(question)
            st.session_state.pending_question = question
            st.session_state.is_generating = True

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            st.rerun()

    if (
        st.session_state.is_generating
        and st.session_state.pending_question is not None
    ):
        current_question = st.session_state.pending_question

        try:
            with st.chat_message("assistant"):
                with st.spinner("AI Study Mate is thinking..."):
                    retrieved_docs = process_chat_question(
                        retriever, current_question
                    )

                    sources = get_chat_sources(retrieved_docs)

                    answer = st.write_stream(
                        stream_chat_answer(
                            document_chain,
                            current_question,
                            retrieved_docs
                        )
                    )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

        except Exception as e:
            st.error(f"Unable to generate the answer: {e}")

        finally:
            st.session_state.is_generating = False
            st.session_state.pending_question = None

        st.rerun()
