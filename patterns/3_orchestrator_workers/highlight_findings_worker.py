import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.bedrock_client import invoke_model, get_completion_from_response
from common.utils import extract_and_load_json

def highlight_key_findings(paper_content):
    prompt = f"""
    Highlight the key findings from the given scientific paper content.
    Return the result as a JSON array of strings, with each string representing a key finding.

    Paper content:
    {paper_content[:1000]}...
    """
    response = invoke_model(prompt)
    return extract_and_load_json(get_completion_from_response(response))

if __name__ == "__main__":
    sample_paper = "The results of our study show that the new algorithm outperforms existing methods..."
    print(highlight_key_findings(sample_paper))