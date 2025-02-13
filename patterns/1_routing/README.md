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

## Running the Gradio Interface

To run the Gradio interface for this pattern:

1. Ensure you have installed the required dependencies, including Gradio:

pip install -r requirements.txt pip install gradio


2. Run the Gradio app:
python gradio_app.py


3. Open your web browser and go to the URL displayed in the console (usually `http://127.0.0.1:7860`).

4. Use the interface to interact with the pattern implementation.

## Expected Output

The script will process multiple inquiries, printing the classification and generated response for each.

## Customization

You can modify the `inquiries` list in the `example.py` file to test different scenarios and languages.


