import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils import (
    create_bedrock_client,
    text_completion,
    extract_json_from_text,
    NOVA_LITE
)

# Create a client once to be reused
bedrock_client = create_bedrock_client()

def classify_inquiry(inquiry):
    prompt = f"""
    Analyze the following customer inquiry. Identify the language and the main topic category.
    Return the result as a JSON object with keys 'language' and 'category'.
    Language should be one of: 'English', 'Spanish', 'French', 'German', 'Danish', 'Swedish' or 'Other'.
    Category should be one of: 'Technical', 'Billing', 'Product', or 'General'.

    Customer Inquiry: "{inquiry}"
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return extract_json_from_text(response)

def technical_support_response(inquiry, language):
    prompt = f"""
    Generate a technical support response in {language} for the following inquiry:
    "{inquiry}"
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return response

def billing_inquiry_response(inquiry, language):
    prompt = f"""
    Generate a billing-related response in {language} for the following inquiry:
    "{inquiry}"
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return response

def product_info_response(inquiry, language):
    prompt = f"""
    Generate a product information response in {language} for the following inquiry:
    "{inquiry}"
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return response

def general_inquiry_response(inquiry, language):
    prompt = f"""
    Generate a general response in {language} for the following inquiry:
    "{inquiry}"
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return response

def route_and_respond(inquiry):
    # Step 1: Classify the inquiry
    classification = classify_inquiry(inquiry)
    print("Classification:", classification)

    # Step 2: Route to the appropriate response generator based on category
    category = classification['category']
    language = classification['language']

    if category == 'Technical':
        response = technical_support_response(inquiry, language)
    elif category == 'Billing':
        response = billing_inquiry_response(inquiry, language)
    elif category == 'Product':
        response = product_info_response(inquiry, language)
    else:  # General
        response = general_inquiry_response(inquiry, language)

    print(f"\nGenerated Response ({language}):\n", response)
    return response

# Example usage
if __name__ == "__main__":
    inquiries = [
        "How do I reset my password?",
        "¿Cuándo vence mi factura?",
        "Quelles sont les caractéristiques du nouveau produit?",
        "Ich habe eine Frage zur Garantie.",
        "Hvordan returnerer jeg et produkt?"
    ]

    for inquiry in inquiries:
        print("\n" + "="*50)
        print(f"Processing inquiry: {inquiry}")
        route_and_respond(inquiry)