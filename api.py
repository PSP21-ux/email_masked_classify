from utils import mask_pii, demask_pii
from models import classify_email_with_gpt
import logging

def process_email(email_body):
    logging.info("Received email for processing")
    
    masked_email, entities = mask_pii(email_body)
    logging.info(f"Masked Email: {masked_email}")
    logging.info(f"Masked Entities: {entities}")

    category = classify_email_with_gpt(masked_email)
    logging.info(f"Email classified as: {category}")

    demasked_email = demask_pii(masked_email, entities)

    return {
        "input_email_body": email_body,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }
