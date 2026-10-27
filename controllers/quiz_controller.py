from services.quiz_service import generate_quiz

def create_quiz(quiz_docs, number_of_questions, llm):
    questions, raw_response = generate_quiz(
        quiz_docs=quiz_docs,
        number_of_questions=number_of_questions,
        llm=llm
    )

    return questions, raw_response