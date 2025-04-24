import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the categories for classification
CATEGORIES = ["Billing Issues", "Technical Support", "Account Management"]

# System prompt to guide the model's behavior
SYSTEM_PROMPT = f"""
You are an intelligent customer support classifier.
Classify the following email into one of these categories:
{', '.join(CATEGORIES)}.
Respond with just the category text.
"""

def classify_email_with_gpt(email_text):
    """
    Classify the given email text into a predefined category using OpenAI's GPT model.
    """
    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": email_text}
            ],
            temperature=0.0
        )
        # Extract and return the category from the response
        category = response.choices[0].message.content.strip()
        if category in CATEGORIES:
            return category
        return "Unknown"
    except Exception as e:
        logging.exception("OpenAI API call failed")
        return "Unknown"
