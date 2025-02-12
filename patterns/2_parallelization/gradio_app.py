import gradio as gr
from example import summarize_review
import concurrent.futures
import time

EXAMPLE_REVIEWS = """This smartphone is amazing! The camera quality is top-notch, and the battery life lasts all day. The screen is vibrant and responsive.
I'm disappointed with this laptop. While it looks sleek, it runs slow and the fan is noisy. The keyboard feels cheap and the trackpad is not very responsive.
These wireless earbuds exceeded my expectations. The sound quality is crisp and clear, with deep bass. They're comfortable to wear for hours.
This smart home device is a game-changer. It's easy to set up and integrates well with other smart devices. The voice recognition is accurate.
The fitness tracker is decent but not great. It accurately counts steps and monitors heart rate, but the sleep tracking seems off. Battery life is good."""

def process_reviews_with_details(reviews):
    review_list = reviews.split('\n')
    start_time = time.time()
    
    progress_output = "Starting parallel processing...\n"
    summaries = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_review = {executor.submit(summarize_review, review): review 
                          for review in review_list}
        
        for future in concurrent.futures.as_completed(future_to_review):
            review = future_to_review[future]
            try:
                summary = future.result()
                summaries.append(summary)
                progress_output += f"\nProcessed review: {review[:50]}...\n"
                progress_output += f"Summary: {summary}\n"
            except Exception as exc:
                progress_output += f"\nError processing review: {review[:50]}...\n"
                progress_output += f"Error: {str(exc)}\n"
    
    end_time = time.time()
    final_output = f"Processed {len(summaries)} reviews in {end_time - start_time:.2f} seconds."
    
    return progress_output, final_output, "\n\n".join(summaries)

iface = gr.Interface(
    fn=process_reviews_with_details,
    inputs=gr.Textbox(
        lines=10, 
        label="Product Reviews (one per line)", 
        value=EXAMPLE_REVIEWS
    ),
    outputs=[
        gr.Textbox(lines=15, label="Processing Progress", elem_classes=["output-box"]),
        gr.Textbox(lines=2, label="Performance Metrics", elem_classes=["output-box"]),
        gr.Textbox(lines=10, label="Final Summaries", elem_classes=["output-box"])
    ],
    title="Product Review Summarization - Parallelization Pattern",
    description="This example demonstrates the parallelization pattern using a product review summarization system. Parallelization in GenAI applications involves processing multiple inputs simultaneously using multiple threads or processes. This can significantly reduce the overall processing time for large numbers of similar tasks. Watch as multiple reviews are processed simultaneously. Try to remove/add reviews and note that processing time stays relatively the same.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()