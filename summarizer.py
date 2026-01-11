from utils.llm import generate_ai

def summarize(text):
    prompt = f"Summarize this in simple bullet points:\n{text}"
    return generate_ai(prompt)