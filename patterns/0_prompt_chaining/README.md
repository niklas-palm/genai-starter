# Prompt Chaining Example: Customer Support Email Generator

This example demonstrates the prompt chaining pattern using a customer support email generator.

## What is Prompt Chaining?

Prompt chaining is a technique where the output of one prompt is used as input for the next prompt in a sequence. This allows for more complex tasks to be broken down into smaller, manageable steps, each building upon the previous one.

## This Example

In this example, we generate a customer support email through three chained prompts:

1. Analyze the customer inquiry
2. Generate response points based on the analysis
3. Craft the final email using the analysis and response points

## How to Run

1. Ensure you have set up your AWS credentials for Bedrock access.
2. Install the required dependencies:

pip install -r requirements.txt

3. Run the script:

python example.py

## Expected Output

The script will print the results of each step (analysis, response points) and the final generated email.

## Customization

You can modify the `customer_inquiry` variable in the `example.py` file to test different scenarios.