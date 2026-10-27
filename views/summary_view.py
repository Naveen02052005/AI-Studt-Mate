
import streamlit as st

from services.summary_service import generate_summary


def render_summary_page(llm):
    st.markdown("## 📝 Summarize")
    st.caption(
        "Turn your study PDFs into clear summaries, "
        "detailed notes, and key points"
    )
    st.divider()

    if "vectorstore" not in st.session_state:
        st.info(
            "Please upload your study PDFs in My Documents first."
        )
        return

    st.success("Your study documents are ready for summarization")

    pdf_names = st.session_state.get("pdf_names", [])

    with st.container(border=True):
        st.markdown("### Summary Settings")
        st.caption(
            "Choose a document and the type of summary you need."
        )

        selected_pdf = st.selectbox(
            "Choose a PDF to summarize",
            pdf_names
        )

        summary_type = st.selectbox(
            "Choose summary type",
            ["Quick Summary", "Detailed Summary", "Key Points"]
        )

    if st.button("Generate Summary"):
        study_documents = st.session_state.study_documents

        study_docs = [
            doc for doc in study_documents
            if doc.metadata.get("source_file") == selected_pdf
        ]

        batch_size = 15

        study_batches = [
            study_docs[i:i + batch_size]
            for i in range(0, len(study_docs), batch_size)
        ]

        progress_text = st.empty()

        with st.spinner("Generating summary..."):
            final_summary_text = generate_summary(
                study_batches=study_batches,
                summary_type=summary_type,
                llm=llm,
                progress_callback=progress_text.write
            )

        progress_text.empty()

        st.divider()

        with st.container(border=True):
            st.markdown("### 📄 Your Summary")
            st.markdown(final_summary_text)

            st.download_button(
                "Download Summary",
                final_summary_text,
                "summary.md",
                "text/markdown"
            )
