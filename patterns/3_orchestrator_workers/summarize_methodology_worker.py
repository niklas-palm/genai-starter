import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.bedrock_client import invoke_model, get_completion_from_response

def summarize_methodology(paper_content):
    prompt = f"""
    Summarize the methodology described in the given scientific paper content.
    Provide a concise summary in 2-3 sentences.

    Paper content:
    {paper_content[:1000]}...
    """
    response = invoke_model(prompt)
    return get_completion_from_response(response)

if __name__ == "__main__":
    sample_paper = "The methodology of this study involved a randomized controlled trial..."
    print(summarize_methodology(sample_paper))