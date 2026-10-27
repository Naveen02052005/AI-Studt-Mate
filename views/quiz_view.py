
import json
import streamlit as st

from controllers.quiz_controller import create_quiz


def render_quiz_page(llm):
    st.markdown("## 🎯 Practice Quiz")

    st.caption(
        "Test your understanding with questions generated "
        "from your uploaded study materials."
    )
    st.divider()

    if not st.session_state.pdf_names:
        st.info("Please upload a PDF in My Documents first.")
        return

    with st.container(border=True):
        st.markdown("### Quiz Settings")
        st.caption(
            "Choose your question count and the study PDF "
            "you want to practice."
        )

        number_of_questions = st.selectbox(
            "Number of questions",
            [5, 10, 15, 20]
        )

        selected_pdf = st.selectbox(
            "Select PDF",
            st.session_state.pdf_names
        )

    quiz_docs = [
        doc for doc in st.session_state.study_documents
        if doc.metadata.get("source_file") == selected_pdf
    ]

    if st.button("🎯 Generate Quiz"):
        try:
            questions, raw_response = create_quiz(
                quiz_docs=quiz_docs,
                number_of_questions=number_of_questions,
                llm=llm
            )

            if questions:
                st.session_state.quiz_questions = questions
                st.session_state.quiz_submitted = False

                st.success(
                    f"{len(questions)} questions generated successfully!"
                )
            else:
                st.warning(
                    "No questions were generated. Please try again."
                )

        except (json.JSONDecodeError, AttributeError) as e:
            st.error(f"Could not read the quiz response: {e}")

    if st.session_state.get("quiz_questions"):
        st.subheader("📝 Answer the Questions")

        for i, question in enumerate(
            st.session_state.quiz_questions
        ):
            st.write(
                f"**Question {i + 1}:** {question['question']}"
            )

            st.radio(
                "Choose your answer:",
                question["options"],
                key=f"quiz_answer_{i}",
                disabled=st.session_state.quiz_submitted
            )

        if st.button(
            "✅ Submit Quiz",
            disabled=st.session_state.quiz_submitted
        ):
            st.session_state.quiz_submitted = True
            st.rerun()

        if st.session_state.quiz_submitted:
            score = 0

            for i, question in enumerate(
                st.session_state.quiz_questions
            ):
                selected_answer = st.session_state.get(
                    f"quiz_answer_{i}"
                )

                if selected_answer == question["correct_answer"]:
                    score += 1

            total_questions = len(st.session_state.quiz_questions)
            percentage = (score / total_questions) * 100

            st.subheader("📊 Quiz Results")
            st.metric("Your Score", f"{score} / {total_questions}")
            st.metric("Percentage", f"{percentage:.1f}%")

            for i, question in enumerate(
                st.session_state.quiz_questions
            ):
                selected_answer = st.session_state.get(
                    f"quiz_answer_{i}"
                )

                st.markdown(
                    f"**Question {i + 1}:** {question['question']}"
                )

                if selected_answer == question["correct_answer"]:
                    st.success("Correct answer!")
                else:
                    st.error("Incorrect answer.")

                st.write(
                    f"**Your answer:** {selected_answer or 'Not answered'}"
                )
                st.write(
                    f"**Correct answer:** {question['correct_answer']}"
                )
                st.write(
                    f"**Explanation:** {question['explanation']}"
                )
                st.divider()
