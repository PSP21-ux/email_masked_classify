import re
import logging

PII_PATTERNS = {
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "phone_number": r"\b(?:\+91[-\s]?)?[789]\d{9}\b",
    "aadhar_num": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "credit_debit_no": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "cvv_no": r"\b\d{3}\b(?![-\s]?\d)",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/(20)?\d{2}\b",
    "dob": r"\b(0?[1-9]|[12][0-9]|3[01])[-/](0?[1-9]|1[0-2])[-/](\d{2,4})\b",
    "full_name": r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b"
}

def mask_pii(text):
    entities = []
    masked_text = text
    offset = 0  # Adjust positions after replacement

    for label, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, masked_text):
            original = match.group()
            start, end = match.start(), match.end()

            # Adjust for previous replacements
            real_start = start + offset
            real_end = end + offset

            placeholder = f"[{label}]"
            masked_text = masked_text[:start] + placeholder + masked_text[end:]
            offset += len(placeholder) - len(original)

            entities.append({
                "position": [real_start, real_end],
                "classification": label,
                "entity": original
            })
            logging.info(f"Masked {label}: {original} -> {placeholder}")

    return masked_text, entities

def demask_pii(masked_text, entities):
    restored_text = masked_text
    for entity in entities:
        placeholder = f"[{entity['classification']}]"
        restored_text = restored_text.replace(placeholder, entity["entity"], 1)
    return restored_text
