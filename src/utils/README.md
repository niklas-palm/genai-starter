# Bedrock Utilities

Utility functions for AWS Bedrock models using the Converse API.

## Functions

- `create_bedrock_client()`: Creates a Bedrock runtime client
- `text_completion()`: Simple text completion tasks
- `read_file()`: Reads media files as bytes
- `invoke_with_media()`: Works with text, images, and videos
- `extract_json_from_text()`: Extracts JSON from model responses
- `generate_conversation()`: Handles multi-turn conversations with optional media
- `stream_conversation()`: Returns model responses as text chunks
- `invoke_with_prefill()`: Guides model responses with prefilled text

## Usage

````python
from utils.bedrock_converse_utils import (
    create_bedrock_client,
    text_completion,
    invoke_with_media,
    invoke_with_prefill
)

# Basic text completion
client = create_bedrock_client()
response = text_completion(
    client=client,
    prompt="Explain quantum computing",
    model_id="us.amazon.nova-lite-v1:0"  # Default model
)

# Working with images
image_response = invoke_with_media(
    client=client,
    prompt="What's in this image?",
    image_path="path/to/image.jpg"
)

# Response prefilling for structured output
prefill_text = '```json\n{\n  "sentiment": "'
sentiment_analysis = invoke_with_prefill(
    client=client,
    prompt="Analyze: 'I loved this product!'",
    prefill=prefill_text
)
print(prefill_text + sentiment_analysis)  # Combine prefill with response
````
