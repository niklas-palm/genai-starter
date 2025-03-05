# GenAI Hackathon Assets

This repository contains lightweight samples that showcase common prompt engineering techniques and design patterns when building generative AI applications with AWS Bedrock.

## Prerequisites

- Active AWS credentials in the environment
- AWS region with Bedrock service access (default: us-west-2)
- Access to the Claude and Nova models in your AWS account.

```bash
pip install -r requirements.txt
```

## Notebooks

Start learning with these notebooks:

### 0_prompt_engineering.ipynb

- Learn prompt engineering fundamentals
- Structure prompts for better results
- Extract structured outputs
- Implement advanced techniques like Chain of Thought and self-verification

### 1_multimodal_inputs.ipynb

- Work with multimodal inputs (text, images, videos)
- Learn image and video analysis with Amazon Bedrock Nova

## Frontend Examples

The `frontend/` directory contains sample Gradio applications demonstrating how to build simple chat interfaces with AWS Bedrock:

- **app.py**: Basic chat application using AWS Bedrock Converse API
- **app_streaming.py**: Identical UI but with real-time token streaming

These examples show how to:

- Create chat interfaces with Gradio
- Manage conversation history
- Implement both standard and streaming responses

To run:

```bash
# Basic chat
python frontend/app.py  # Available at http://127.0.0.1:7861

# Streaming chat
python frontend/app_streaming.py  # Available at http://127.0.0.1:7862
```

## Design Patterns

The `patterns/` directory includes common GenAI design patterns:

### 0_prompt_chaining

- Chain multiple prompts together
- Build complex workflows with sequential steps

### 1_routing

- Implement intelligent routing between different models
- Route requests based on content and skills

### 2_parallelization

- Process multiple requests in parallel
- Aggregate results from multiple model calls

### 3_evaluator_optimizer

- Implement self-evaluation techniques
- Optimize outputs based on evaluation criteria

## Utility Functions

The repository includes centralized utility functions in `src/utils/bedrock_converse_utils.py`:

- `create_bedrock_client`: Create a Bedrock client
- `text_completion`: Send basic text prompts
- `invoke_with_media`: Unified function for text, images, and videos
- `generate_conversation`: Create conversations with history
- `stream_conversation`: Stream model responses in real-time
- `extract_json_from_text`: Extract structured data from responses
