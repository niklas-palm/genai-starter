# Evaluator-Optimizer Pattern Example: Email Subject Line Generator

This example demonstrates the evaluator-optimizer pattern using an automated email subject line generator for marketing campaigns.

## What is the Evaluator-Optimizer Pattern?

The evaluator-optimizer pattern involves generating multiple outputs, evaluating their quality based on specific criteria, and then using that evaluation to inform and improve future generations. This creates a feedback loop that can lead to increasingly better results.

## This Example

In this example, we have three main components:

1. **Generator**: Creates multiple email subject line options.
2. **Evaluator**: Assesses each subject line based on relevance, catchiness, clarity, and urgency.
3. **Optimizer**: Manages the process of generation, evaluation, and improvement over multiple iterations.

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

The script will run through multiple iterations of generating and evaluating subject lines. For each iteration, it will display:
- Generated subject lines and their scores
- Feedback for improvement
- The best subject line and its score after all iterations

## Customization

You can modify the `email_content` in the script to test with different email campaigns. You can also adjust the number of iterations and options per iteration in the `optimizer.optimize()` method call.