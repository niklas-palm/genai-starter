import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils import (
    create_bedrock_client,
    generate_conversation,
    extract_json_from_text,
    NOVA_LITE
)

# Create a client once to be reused
bedrock_client = create_bedrock_client()

# System prompt for improved consistency across all interactions
SYSTEM_PROMPT = """
You are an AI assistant helping with customer service tasks.
Always provide factual, helpful responses.
When asked to return JSON, format it properly within ```json code blocks.
"""

def classify_inquiry(inquiry):
    prompt = f"""
    Analyze the following customer inquiry. Identify the language and the main topic category.
    Return the result as a JSON object with keys 'language' and 'category'.
    Language should be one of: 'English', 'Spanish', 'French', 'German', 'Danish', 'Swedish' or 'Other'.
    Category should be one of: 'Technical', 'Billing', 'Product', or 'General'.

    Customer Inquiry: "{inquiry}"
    """
    response = generate_conversation(
        client=bedrock_client,
        prompt=prompt,
        model_id=NOVA_LITE,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Extract text from response
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return extract_json_from_text(content["text"])

def generate_response(inquiry, language, category):
    """
    Unified response generator with routing handled via the prompt.
    This simplifies the code by using a single function instead of four separate ones.
    """
    # Create a prompt based on the category
    category_instructions = {
        "Technical": "Provide troubleshooting steps and technical instructions.",
        "Billing": "Explain billing policies, payment options, and account information.",
        "Product": "Describe product features, specifications, and usage instructions.",
        "General": "Provide general information and friendly guidance."
    }
    
    instructions = category_instructions.get(category, category_instructions["General"])
    
    prompt = f"""
    Generate a {category.lower()}-related response in {language} for the following inquiry:
    "{inquiry}"
    
    Additional instructions: {instructions}
    """
    
    response = generate_conversation(
        client=bedrock_client,
        prompt=prompt,
        model_id=NOVA_LITE,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Extract text from response
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return content["text"]

def route_and_respond(inquiry):
    # Step 1: Classify the inquiry
    classification = classify_inquiry(inquiry)
    print("Classification:", classification)

    # Step 2: Route to the appropriate response generator based on category
    category = classification['category']
    language = classification['language']
    
    # Use the unified response generator with the appropriate parameters
    response = generate_response(inquiry, language, category)
    
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