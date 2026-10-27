
import json

from services.prompts import QUIZ_PROMPT


def generate_quiz(quiz_docs, number_of_questions, llm):
    quiz_material = "\n\n".join(
        doc.page_content for doc in quiz_docs
    )

    if not quiz_material.strip():
        return [], ""

    quiz_response = (QUIZ_PROMPT | llm).invoke({
        "number_of_questions": number_of_questions,
        "study_material": quiz_material
    })

    response_text = quiz_response.text.strip()

    # Remove Markdown code fences if Gemini adds them
    if response_text.startswith("```json"):
        response_text = response_text[len("```json"):]

    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    if not response_text:
        return [], quiz_response.text

    quiz_data = json.loads(response_text)
    questions = quiz_data.get("questions", [])

    return questions, quiz_response.text
