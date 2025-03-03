# Bedrock Text Completion Frontend

A lightweight Gradio interface for AWS Bedrock text completions.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure you have proper AWS credentials configured with Bedrock access.

## Running the App

To start the Gradio app:

```bash
# Run from the project root directory, not inside the frontend folder
python frontend/app.py
```

The app will be available at http://127.0.0.1:7860 in your browser.

## Features

- Simple text completion using AWS Bedrock models
- Support for multiple models (Claude 3.5 Sonnet, Claude 3.5 Haiku, Nova Lite, Nova Pro)
- Adjustable temperature parameter