import os
import io
import hashlib
import streamlit as st


from services.document_service import load_pdf_documents,create_vectorstore
from types import SimpleNamespace


BASE_UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "uploaded_pdfs"
)


def get_session_upload_dir():
    upload_dir = os.path.join(
        BASE_UPLOAD_DIR,
        st.session_state.session_id
    )
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


def get_saved_pdf_names(upload_dir):
    return [
        filename
        for filename in os.listdir(upload_dir)
        if filename.lower().endswith(".pdf")
        and os.path.isfile(os.path.join(upload_dir, filename))
    ]


def render_documents_page(text_splitter, embeddings):
    upload_dir = get_session_upload_dir()
    st.markdown("## 📚 My Documents")
    st.caption("Manage your study materials in one place")
    st.write("")
   

    with st.container(border=True):
        st.markdown("### 📤 Upload study materials")
        st.write(
            "Add your PDF notes, textbooks, or study guides "
            "to use them with AI Study Mate."
        )

        uploaded_files = st.file_uploader(
            "Upload your study PDFs",
            type="pdf",
            accept_multiple_files=True,
            help="You can upload multiple PDF files",
            key=f"pdf_uploader_{st.session_state.get('uploader_version',0)}"
        )
    
    # Save newly selected PDFs to local storage
    if uploaded_files:
        upload_signature = tuple(
            (
                file.name,
                hashlib.sha256(file.getvalue()).hexdigest()
            )
            for file in uploaded_files
        )

        if upload_signature != st.session_state.get(
            "last_upload_signature"
        ):
            for uploaded_pdf in uploaded_files:
                safe_filename = os.path.basename(uploaded_pdf.name)
                saved_path = os.path.join(upload_dir, safe_filename)

                with open(saved_path, "wb") as pdf_file:
                    pdf_file.write(uploaded_pdf.getvalue())

            st.session_state.last_upload_signature = upload_signature

            st.rerun()

    # Clear all documents with confirmation

    if get_saved_pdf_names(upload_dir):
        if st.button("🗑️ Clear All Documents", key="clear_all_documents"):
            st.session_state.confirm_clear_documents = True

        if st.session_state.get("confirm_clear_documents", False):
            st.warning(
                "Are you sure? This will permanently delete all saved PDFs."
            )

            confirm_col, cancel_col = st.columns(2)

            with confirm_col:
                if st.button("Yes, Clear All", key="confirm_clear_all"):
                    for filename in get_saved_pdf_names(upload_dir):
                        file_path = os.path.join(upload_dir, filename)

                        if os.path.isfile(file_path):
                            os.remove(file_path)

                    keys_to_clear = [
                        "vectorstore",
                        "study_documents",
                        "pdf_signature",
                        "pdf_names",
                        "document_details",
                        "messages",
                        "pending_question",
                        "quiz_questions",
                        "quiz_submitted",
                        "last_upload_signature",
                    ]

                    for key in keys_to_clear:
                        st.session_state.pop(key, None)

                    st.session_state.confirm_clear_documents = False
                    st.session_state.uploader_version = (
                        st.session_state.get("uploader_version", 0) + 1
                    )

                    st.rerun()

            with cancel_col:
                if st.button("Cancel", key="cancel_clear_all"):
                    st.session_state.confirm_clear_documents = False
                    st.rerun()

    # Get all saved PDFs, including previously uploaded files
    saved_pdf_names = sorted(get_saved_pdf_names(upload_dir))

    pdf_signature = tuple(
        (
            filename,
            hashlib.sha256(
                open(
                    os.path.join(upload_dir, filename), "rb"
                ).read()
            ).hexdigest()
        )
        for filename in saved_pdf_names
    )

    # Reprocess only when the saved PDF collection changes
    if (
        saved_pdf_names
        and st.session_state.get("pdf_signature") != pdf_signature
    ):
        with st.spinner("Processing your PDFs..."):
            all_docs = []
            failed_files = []
            document_details = []

            for pdf_name in saved_pdf_names:
                saved_path = os.path.join(upload_dir, pdf_name)

                try:
                    with open(saved_path, "rb") as pdf_file:
                        pdf_content = pdf_file.read()

                    saved_pdf = SimpleNamespace(
                        name=pdf_name,
                        getvalue=lambda content=pdf_content: content
                    )

                    docs = load_pdf_documents(saved_pdf)

                    if not docs:
                        failed_files.append(
                            f"{pdf_name}: No extractable text found."
                        )
                        
                        # Delete the empty file
                        if os.path.isfile(saved_path):
                            os.remove(saved_path)

                        continue

                    for doc in docs:
                        doc.metadata["source_file"] = pdf_name

                    all_docs.extend(docs)

                    document_details.append({
                        "name": pdf_name,
                        "pages": len(docs),
                        "status": "Ready"
                    })

                except Exception as e:
                    failed_files.append(f"{pdf_name}: {e}")
                    if os.path.isfile(saved_path):
                        os.remove(saved_path)

            if failed_files:
                with st.expander("PDF Processing Warnings"):
                    for error in failed_files:
                        st.warning(error)

            if all_docs:
                documents = text_splitter.split_documents(all_docs)

                if documents:
                    st.session_state.vectorstore = create_vectorstore(
                        documents, embeddings
                    )
                    st.session_state.study_documents = documents
                    st.session_state.pdf_signature = pdf_signature
                    st.session_state.pdf_names = [
                        item["name"] for item in document_details
                    ]
                    st.session_state.document_details = document_details
                    st.session_state.messages = []
                    st.session_state.pending_question = None
                else:
                    st.error("No document chunks were created.")
            else:
                st.error(
                    "No readable text was found in the saved PDFs."
                )

    # Display document cards
    document_details = st.session_state.get(
        "document_details", []
    )

    if document_details:
        st.subheader("Your uploaded documents")
        st.write("Your study materials are ready to use")

        st.caption(
            f"{len(document_details)} document(s) processed successfully."
        )

        for start in range(0, len(document_details), 2):
            columns = st.columns(2)

            for offset, column in enumerate(columns):
                index = start + offset

                if index >= len(document_details):
                    break

                document = document_details[index]

                with column:
                    with st.container(border=True):
                        st.markdown(f"### 📄 Document {index + 1}")
                        st.markdown(f"**{document['name']}**")
                        st.caption(
                            f"Pages indexed: {document['pages']}"
                        )
                        st.success("Ready for Ask AI")

                        
                        if st.button("ASK AI", key=f"ask_ai_{index}"):
                            st.session_state.page = "Ask AI"
                            st.rerun()

                        
                        if st.button(
                            "🗑️ Remove",
                            key=f"remove_pdf_{index}"
                        ):
                            saved_path = os.path.join(
                                upload_dir,
                                document["name"]
                            )

                            # Delete the selected PDF file
                            if os.path.isfile(saved_path):
                                os.remove(saved_path)

                            # Remove it from the displayed document list
                            st.session_state.document_details = [
                                item
                                for item in st.session_state.get(
                                    "document_details", []
                                )
                                if item["name"] != document["name"]
                            ]

                            st.session_state.pdf_names = [
                                name
                                for name in st.session_state.get(
                                    "pdf_names", []
                                )
                                if name != document["name"]
                            ]

                            # Remove its content from the study documents
                            remaining_docs = [
                                doc
                                for doc in st.session_state.get(
                                    "study_documents", []
                                )
                                if doc.metadata.get("source_file")
                                != document["name"]
                            ]

                            if remaining_docs:
                                st.session_state.study_documents = (
                                    remaining_docs
                                )
                                st.session_state.vectorstore = (
                                    create_vectorstore(
                                        remaining_docs,
                                        embeddings
                                    )
                                )
                            else:
                                for key in [
                                    "vectorstore",
                                    "study_documents",
                                    "pdf_signature",
                                    "pdf_names",
                                    "document_details",
                                ]:
                                    st.session_state.pop(key, None)

                            # Reset the uploader so the removed PDF
                            # is not uploaded again automatically
                            st.session_state.last_upload_signature = None
                            st.session_state.uploader_version = (
                                st.session_state.get(
                                    "uploader_version", 0
                                ) + 1
                            )

                            st.session_state.messages = []
                            st.session_state.pending_question = None

                            st.rerun()


                            st.session_state.messages = []
                            st.session_state.pending_question = None

                            st.success(f"Removed {document['name']}")
                            st.rerun()


    else:
        st.info(
            "No documents uploaded yet. "
            "Use the uploader above to add your study PDFs. "
            "Once processed, your documents will appear here."
        )
