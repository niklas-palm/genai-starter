# Parallelization Example: Product Review Summarization

This example demonstrates the parallelization pattern using a product review summarization system.

![overview](diagram.png)

## What is Parallelization?

Parallelization in GenAI applications involves processing multiple inputs simultaneously using multiple threads or processes. This can significantly reduce the overall processing time for large numbers of similar tasks.

## This Example

In this example, we parallelize the summarization of multiple product reviews:

1. Define a function to summarize a single review
2. Use ThreadPoolExecutor to process multiple reviews in parallel
3. Collect and display the results

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

The script will process multiple reviews in parallel, printing each review and its summary as they complete.

## Customization

You can modify the `reviews` list in the `example.py` file to test with different reviews or increase the number of reviews to see the benefits of parallelization more clearly.

## Note on Parallelization

While this example uses threading, the actual performance improvement may be limited by API rate limits or the specific GenAI model's capacity. In a production environment, you might need to implement more sophisticated parallelization techniques or queue systems to handle larger volumes efficiently.
