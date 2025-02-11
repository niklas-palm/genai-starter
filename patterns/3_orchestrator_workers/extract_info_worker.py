import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.bedrock_client import invoke_model, get_completion_from_response
from common.utils import extract_and_load_json

def extract_key_info(paper_content):
    prompt = f"""
    Extract the following key information from the given scientific paper content:
    1. Title
    2. Authors (as a list)
    3. Abstract

    Return the result as a JSON object with keys 'title', 'authors', and 'abstract'.

    Paper content:
    {paper_content[:1000]}...
    """
    response = invoke_model(prompt)
    return extract_and_load_json(get_completion_from_response(response))

if __name__ == "__main__":
    # This allows the worker to be run independently for testing
    sample_paper = "Title: Advanced Machine Learning Techniques\nAuthors: John Doe, Jane Smith\nAbstract: This paper explores..."
    print(extract_key_info(sample_paper))