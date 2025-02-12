import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import concurrent.futures
from common.bedrock_client import invoke_model, get_completion_from_response

def summarize_review(review):
    prompt = f"""
    Summarize the following product review in one sentence:
    "{review}"
    """
    response = invoke_model(prompt)
    return get_completion_from_response(response)

def summarize_reviews_parallel(reviews):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_review = {executor.submit(summarize_review, review): review for review in reviews}
        summaries = []
        for future in concurrent.futures.as_completed(future_to_review):
            review = future_to_review[future]
            try:
                summary = future.result()
                summaries.append(summary)
                print(f"Review: {review[:50]}...")
                print(f"Summary: {summary}\n")
            except Exception as exc:
                print(f"Review: {review[:50]}... generated an exception: {exc}")
    return summaries

# Example usage
if __name__ == "__main__":
    reviews = [
        "This smartphone is amazing! The camera quality is top-notch, and the battery life lasts all day. The screen is vibrant and responsive. It's a bit pricey, but worth every penny for the features you get.",
        "I'm disappointed with this laptop. While it looks sleek, it runs slow and the fan is noisy. The keyboard feels cheap and the trackpad is not very responsive. Save your money and look for something better.",
        "These wireless earbuds exceeded my expectations. The sound quality is crisp and clear, with deep bass. They're comfortable to wear for hours, and the battery life is impressive. The noise cancellation feature works great in noisy environments.",
        "This smart home device is a game-changer. It's easy to set up and integrates well with other smart devices. The voice recognition is accurate, and it can control lights, thermostats, and even order groceries. However, it sometimes activates when not called upon.",
        "The fitness tracker is decent but not great. It accurately counts steps and monitors heart rate, but the sleep tracking seems off. The app is user-friendly, but syncing can be slow at times. Battery life is good, lasting about a week on a single charge."
    ]

    print("Starting parallel review summarization...\n")
    summaries = summarize_reviews_parallel(reviews)
    print(f"\nProcessed {len(summaries)} reviews in parallel.")