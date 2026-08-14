from app.prompts import build_rag_prompt

context = """
Employees receive 18 days of annual leave.

Unused leave expires after one year.
"""

question = "How many leave days do employees receive?"

prompt = build_rag_prompt(
    question,
    context,
)

print(prompt)