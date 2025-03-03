import gradio as gr
import sys
import os

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import (
    create_bedrock_client,
    text_completion,
    CLAUDE_3_5_SONNET,
    CLAUDE_3_5_HAIKU,
    NOVA_LITE,
    NOVA_PRO,
)

# Create a Bedrock client
bedrock_client = create_bedrock_client()

EXAMPLE_PROMPT = """Explain quantum computing in simple terms."""


def generate_completion(prompt, _history):
    """Generate text completion using Bedrock model"""
    response = text_completion(
        client=bedrock_client,
        prompt=prompt,
        model_id=NOVA_LITE,
    )
    return response


if __name__ == "__main__":

    gr.ChatInterface(
        fn=generate_completion,
        type="messages",
    ).launch(server_port=7861)
