import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.bedrock_client import invoke_model, get_completion_from_response
from common.utils import extract_and_load_json

def identify_topics(paper_content):
    prompt = f"""
    Identify the main topics and keywords from the given scientific paper content.
    Return the result as a JSON object with keys 'main_topics' (list) and 'keywords' (list).

    Paper content:
    {paper_content[:1000]}...
    """
    response = invoke_model(prompt)
    return extract_and_load_json(get_completion_from_response(response))

if __name__ == "__main__":
    sample_paper = "This paper discusses advanced machine learning techniques..."
    print(identify_topics(sample_paper))