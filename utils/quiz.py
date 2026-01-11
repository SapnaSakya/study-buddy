from utils.llm import generate_ai

def generate_quiz(text):
    prompt = f"Generate 5 MCQ questions with options from:\n{text}"
    return generate_ai(prompt)