import os
import google.generativeai as genai
from dotenv import load_dotenv

# load API key from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# setup gemini if the key exists
if GEMINI_API_KEY and GEMINI_API_KEY.strip() != "your_api_key_here" and GEMINI_API_KEY.strip() != "":
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
else:
    AI_ENABLED = False

# simple keyword fallback if gemini fails or isn't set up
FALLBACK_CATEGORIES = {
    "Food & Dining": ["food", "lunch", "dinner", "breakfast", "groceries", "coffee", "restaurant", "burger", "pizza"],
    "Transport": ["uber", "lyft", "taxi", "bus", "train", "flight", "gas", "fuel", "car", "subway", "transit"],
    "Entertainment": ["movie", "cinema", "game", "concert", "netflix", "spotify", "ticket", "event"],
    "Shopping": ["clothes", "amazon", "shoes", "electronics", "mall", "store"],
    "Utilities": ["electricity", "water", "internet", "phone", "bill", "rent", "insurance"],
    "Health": ["doctor", "medicine", "pharmacy", "clinic", "gym", "fitness"]
}

def categorize_expense(description: str) -> str:
    # try the AI first
    if AI_ENABLED:
        try:
            prompt = f"Categorize the following expense description into a single short category name (e.g., Food & Dining, Transport, Entertainment, Utilities, Shopping, Health, etc.). Just return the category name, nothing else.\n\nDescription: {description}"
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
        except Exception:
            # if gemini is down or fails, just fallback to keywords silently
            pass

    # fallback keyword matching
    desc_lower = description.lower()
    for category, keywords in FALLBACK_CATEGORIES.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category
            
    return "Miscellaneous"
# TODO: expand offline NLP dictionary
