import logging
from openai import OpenAI

# Initialize OpenAI client with hardcoded API key
client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

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

    Parameters:
        email_text (str): The email content to classify.

    Returns:
        str: The category assigned to the email.
    """
    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": email_text}
            ],
            temperature=0.0
        )
        # Extract and return the category from the response
        category = response.choices[0].message.content.strip()
        return category
    except Exception as e:
        logging.exception("OpenAI API call failed")
        return "Unknown"
