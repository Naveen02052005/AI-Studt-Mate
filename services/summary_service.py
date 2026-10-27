
from services.prompts import BATCH_SUMMARY_PROMPT, FINAL_SUMMARY_PROMPT


def generate_summary(study_batches, summary_type, llm, progress_callback=None):
    # Create the chain for summarizing individual batches
    batch_summary_chain = BATCH_SUMMARY_PROMPT | llm

    batch_summaries = []

    # Summarize each batch separately
    for batch_number, batch_docs in enumerate(study_batches, start=1):
        batch_material = "\n\n".join(
            doc.page_content for doc in batch_docs
        )

        if progress_callback:
            progress_callback(
                f"Summarizing batch {batch_number} of {len(study_batches)}..."
            )

        batch_response = batch_summary_chain.invoke({
            "summary_type": summary_type,
            "study_material": batch_material
        })

        batch_summaries.append(batch_response.text)

    # Combine all batch summaries into one final summary
    final_summary_chain = FINAL_SUMMARY_PROMPT | llm

    final_response = final_summary_chain.invoke({
        "summary_type": summary_type,
        "batch_summaries": "\n\n".join(batch_summaries)
    })

    return final_response.text
