import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_groq_key():
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key.strip()
    return None


def call_llm(prompt: str) -> str:
    api_key = get_groq_key()

    if not api_key:
        return "LLM_ERROR: GROQ_API_KEY not found in .env file."

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional enterprise document intelligence assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=700,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM_ERROR: {str(e)}"


def build_retrieval_answer(question: str, retrieved_chunks: list[dict], risk_text: str) -> str:
    if not retrieved_chunks:
        return "I could not find relevant information in the uploaded document."

    best_context = retrieved_chunks[0]["text"][:1200]
    score = retrieved_chunks[0]["score"]

    return (
        f"Groq AI is not available, so fallback retrieval answer is shown.\n\n"
        f"Retrieval score: {score:.3f}\n\n"
        f"Relevant document extract:\n\n{best_context}\n\n"
        f"Risk note: {risk_text}"
    )


def generate_answer(question: str, retrieved_chunks: list[dict], risk_text: str) -> str:
    context = "\n\n".join([item["text"][:900] for item in retrieved_chunks])

    prompt = f"""
Answer the user's question using only the document context.

Question:
{question}

Document context:
{context}

Risk analysis:
{risk_text}

Give a clear professional answer.
"""

    response = call_llm(prompt)

    if response and not response.startswith("LLM_ERROR"):
        return response

    return response + "\n\n" + build_retrieval_answer(question, retrieved_chunks, risk_text)


def generate_summary(document_text: str, entities_preview: str, risk_text: str) -> str:
    prompt = f"""
Create an executive summary of this uploaded business document.

Include:
1. Document Overview
2. Important Business Entities
3. Key Clauses or Topics
4. Risk Observations
5. Recommended Actions

Document:
{document_text[:4000]}

Entities:
{entities_preview}

Risk:
{risk_text}
"""

    response = call_llm(prompt)

    if response and not response.startswith("LLM_ERROR"):
        return response

    return response + f"""

# Fallback Executive Summary

The uploaded document has been processed through the document intelligence pipeline.

## Risk Observation

{risk_text}

## Recommended Actions

- Review important clauses manually.
- Use Document Q&A for deeper inspection.
- Download entity and clause reports.
"""