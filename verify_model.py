
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)

def test_model():
    model_name = "roberta-base-openai-detector" # Or the path if local
    try:
        pipe = pipeline("text-classification", model=model_name)
    except Exception:
        # Fallback to a common one if the specific one isn't found or local path issue
        # Assuming the user has it cached or internet access. 
        # If not, I might need to rely on the existing code's behavior.
        # But the user ran the app, so it must be there.
        # Let's try to load from the cache path seen in the logs if possible, 
        # but 'roberta-base-openai-detector' should work if it's in the cache.
        print("Could not load model by name, trying to rely on logic deduction.")
        return

    human_text = "The quick brown fox jumps over the lazy dog."
    ai_text = "As an AI language model, I cannot provide that information."

    print(f"Testing Model: {model_name}")
    
    res_human = pipe(human_text)[0]
    print(f"Human Text: '{human_text}' -> {res_human}")

    res_ai = pipe(ai_text)[0]
    print(f"AI Text: '{ai_text}' -> {res_ai}")

if __name__ == "__main__":
    test_model()
