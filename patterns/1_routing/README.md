# Routing Example: Multi-lingual Customer Inquiry Classifier and Router

This example demonstrates the routing pattern using a multi-lingual customer inquiry system.

## What is Routing?

Routing in the context of GenAI applications involves directing inputs to different models or processes based on certain criteria. This allows for more specialized and efficient handling of diverse inputs.

## This Example

In this example, we route customer inquiries based on their language and topic:

1. Classify the inquiry by language and topic
2. Route to a specialized response generator based on the classification

## How to Run

1. Ensure you have set up your AWS credentials for Bedrock access.
2. Install the required dependencies:

pip install -r requirements.txt

3. Run the script:

python example.py

## Expected Output

The script will process multiple inquiries, printing the classification and generated response for each.

## Customization

You can modify the `inquiries` list in the `example.py` file to test different scenarios and languages.


