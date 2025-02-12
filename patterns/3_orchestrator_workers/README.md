# Orchestrator-Workers Pattern Example: Multi-Stage Document Analysis Pipeline

This example demonstrates the orchestrator-workers pattern using a multi-stage document analysis system for scientific papers.

## What is the Orchestrator-Workers Pattern?

The orchestrator-workers pattern involves a central coordinator (orchestrator) that manages and distributes tasks to multiple specialized workers. Each worker is responsible for a specific task, and the orchestrator handles the overall workflow and coordination.

## This Example

In this example, we have an orchestrator that manages the analysis of scientific papers through four stages:

1. Extract key information (title, authors, abstract)
2. Identify main topics and keywords
3. Summarize the methodology
4. Highlight key findings

Each stage is handled by a separate worker, and the orchestrator coordinates the entire process.

## How to Run

1. Ensure you have set up your AWS credentials for Bedrock access.
2. Install the required dependencies:

pip install -r requirements.txt

3. Run the orchestrator script:

python orchestrator.py

## Running the Gradio Interface

To run the Gradio interface for this pattern:

1. Ensure you have installed the required dependencies, including Gradio:

pip install -r requirements.txt pip install gradio


2. Run the Gradio app:
python gradio_app.py


3. Open your web browser and go to the URL displayed in the console (usually `http://127.0.0.1:7860`).

4. Use the interface to interact with the pattern implementation.

## Expected Output

The script will process sample documents, displaying the results from each stage of the analysis for each document.

## Customization

You can modify the `sample_documents` list in the `orchestrator.py` file to test with different scientific papers. You can also add more worker scripts for additional analysis stages.

## Note on Scalability

This example uses threading for simplicity, but in a production environment, you might use distributed systems, message queues, or serverless functions to handle larger workloads and provide better scalability and fault tolerance.