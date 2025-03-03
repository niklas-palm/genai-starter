import gradio as gr
import sys
import os

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

# Available models to choose from
MODELS = {
    "Claude 3.5 Sonnet": CLAUDE_3_5_SONNET,
    "Claude 3.5 Haiku": CLAUDE_3_5_HAIKU,
    "Nova Lite": NOVA_LITE,
    "Nova Pro": NOVA_PRO,
}


def generate_completion(prompt, model_name, temperature):
    """Generate text completion using Bedrock model"""
    model_id = MODELS[model_name]
    response = text_completion(
        client=bedrock_client, prompt=prompt, model_id=model_id, temperature=temperature
    )
    return response


# Create Gradio interface
iface = gr.Interface(
    fn=generate_completion,
    inputs=[
        gr.Textbox(
            lines=5,
            label="Prompt",
            placeholder="Enter your prompt here...",
            value="Explain quantum computing in simple terms.",
        ),
        gr.Dropdown(
            choices=list(MODELS.keys()), label="Model", value="Claude 3.5 Sonnet"
        ),
        gr.Slider(minimum=0.0, maximum=1.0, step=0.1, value=0.0, label="Temperature"),
    ],
    outputs=gr.Textbox(lines=10, label="Response"),
    title="Bedrock AI Text Completion",
    description="A simple interface for generating text completions using AWS Bedrock models.",
    allow_flagging="never",
)

if __name__ == "__main__":
    iface.launch()
