from utils.llm import generate_ai

def generate_flashcards(text):
    prompt = f"Create flashcards in Question and Answer format from:\n{text}"
    return generate_ai(prompt)