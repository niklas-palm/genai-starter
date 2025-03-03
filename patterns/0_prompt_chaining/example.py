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

def analyze_inquiry(inquiry):
    prompt = f"""
    Analyze the following customer inquiry. Identify the main issue and the customer's sentiment.
    Return the result as a JSON object with keys 'main_issue' and 'sentiment'.

    Customer Inquiry: "{inquiry}"
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return extract_json_from_text(response)

def generate_response_points(analysis):
    prompt = f"""
    Based on the following analysis of a customer inquiry, generate a list of 3-5 key points to address in the response.
    Return the result as a JSON array of strings.

    Analysis: {analysis}
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return extract_json_from_text(response)

def craft_email(analysis, points):
    prompt = f"""
    Craft a personalized customer support email based on the following analysis and key points.
    The email should address the customer's concerns, match their sentiment, and provide helpful information.

    Analysis: {analysis}
    Key Points: {points}

    Begin the email with 'Dear Customer,' and end it with 'Best regards, Customer Support Team'.
    """
    response = text_completion(bedrock_client, prompt, model_id=NOVA_LITE)
    return response

def generate_support_email(customer_inquiry):
    # Step 1: Analyze the inquiry
    analysis = analyze_inquiry(customer_inquiry)
    print("Analysis:", analysis)

    # Step 2: Generate response points
    points = generate_response_points(analysis)
    print("Response Points:", points)

    # Step 3: Craft the email
    email = craft_email(analysis, points)
    print("\nGenerated Email:\n", email)

    return email

# Example usage
if __name__ == "__main__":
    customer_inquiry = "I've been waiting for my order for over a week now, and it still hasn't arrived. This is unacceptable! Can you tell me where my package is and why it's taking so long?"
    generate_support_email(customer_inquiry)