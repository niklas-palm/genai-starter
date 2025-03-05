import gradio as gr
import sys
import os
import queue
import threading

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import (
    create_bedrock_client,
    stream_conversation,
    NOVA_LITE,
)

# Create a Bedrock client
bedrock_client = create_bedrock_client()

EXAMPLE_PROMPTS = [
    "Explain quantum computing in simple terms.",
    "Explain prompt engineering to a five year old",
    "In 2 sentences, what's your take on the meaning of life?",
]


def generate_streaming_response(prompt, history):
    """
    Generate streaming text response using Bedrock's Converse API
    with true token-by-token streaming from the model to the UI.
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
    
    # Create a queue to communicate between the streaming thread and the generator
    token_queue = queue.Queue()
    
    # This will signal when the streaming is complete
    done_streaming = threading.Event()
    
    # Callback function that will be called by stream_conversation
    def handle_token(token):
        token_queue.put(token)
    
    # Run the streaming in a background thread
    def stream_thread():
        stream_conversation(
            client=bedrock_client,
            prompt=prompt,
            model_id=NOVA_LITE,
            system_prompt="You are a helpful, friendly AI assistant.",
            conversation_history=conversation_history,
            callback=handle_token,  # Pass our callback function
        )
        # Signal that streaming is complete
        done_streaming.set()
    
    # Start the streaming thread
    threading.Thread(target=stream_thread, daemon=True).start()
    
    # Generate function that yields tokens as they come in
    partial_response = ""
    
    # Keep yielding until we've received all tokens
    while not done_streaming.is_set() or not token_queue.empty():
        try:
            # Get the next token (timeout to check if we're done)
            token = token_queue.get(timeout=0.05)
            partial_response += token
            yield partial_response
        except queue.Empty:
            # No tokens available right now, check if we're done
            continue


if __name__ == "__main__":
    gr.ChatInterface(
        fn=generate_streaming_response,
        examples=EXAMPLE_PROMPTS,
        title="Bedrock Converse API Chat with Streaming",
        description="Chat example using AWS Bedrock Converse API with real-time token streaming.",
    ).queue().launch(server_port=7862)