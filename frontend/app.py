import gradio as gr
import sys
import os

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import (
    create_bedrock_client,
    generate_conversation,
    NOVA_LITE,
)

# Create a Bedrock client
bedrock_client = create_bedrock_client()

EXAMPLE_PROMPTS = [
    "Explain quantum computing in simple terms.",
    "Explain prompt engineering to a five year old",
    "In 2 sentences, what's your take on the meaning of life?",
]


def generate_response(prompt, history):
    """
    Generate text response using Bedrock's Converse API (non-streaming)
    """
    # Format conversation history for the Converse API
    conversation_history = []
    
    if history:
        for user_msg, assistant_msg in history:
            conversation_history.append(
                {"role": "user", "content": [{"text": user_msg}]}
            )
            if assistant_msg:
                conversation_history.append(
                    {"role": "assistant", "content": [{"text": assistant_msg}]}
                )
    
    # Get the response from the model using generate_conversation
    response = generate_conversation(
        client=bedrock_client,
        prompt=prompt,
        model_id=NOVA_LITE,
        system_prompt="You are a helpful, friendly AI assistant.",
        temperature=0.7,
        conversation_history=conversation_history,
    )
    
    # Extract the text from the response
    output_message = response["output"]["message"]
    text_response = ""
    
    for content in output_message["content"]:
        if "text" in content:
            text_response = content["text"]
            break
    
    # Return the complete response (no streaming)
    return text_response


if __name__ == "__main__":
    gr.ChatInterface(
        fn=generate_response,
        examples=EXAMPLE_PROMPTS,
        title="Bedrock Converse API Chat (Non-Streaming)",
        description="Basic chat example using AWS Bedrock Converse API without streaming.",
    ).queue().launch(server_port=7861)