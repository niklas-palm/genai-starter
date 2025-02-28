# GenAI Hackathon Assets

This repository contains lightweight samples that showcase common design patterns when building generative AI applications. It's designed to help developers go from zero to hero with iterative, easy-to-follow steps.

## Overview

This repository provides a progressive approach to learning generative AI with Amazon Bedrock. Each notebook builds on skills from the previous one, allowing you to incrementally develop your GenAI skills.

1. **0_prompt_engineering.ipynb**: Learn the basics of prompt engineering, structuring prompts, and getting structured outputs
2. **1_multimodal_inputs.ipynb**: Explore working with text, images, and videos using Amazon Bedrock Nova
3. **patterns/**: Explore common design patterns for GenAI applications:
   - Prompt chaining
   - Routing
   - Parallelization
   - Orchestration with workers
   - Evaluation and optimization
   - Agents and multi-agent systems

## Prerequisites

- Active AWS credentials in the environment
- AWS region with Bedrock service access (default: us-west-2)
- Access to the models used in the notebooks (Claude and Nova)

## Usage

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Navigate through the notebooks in numerical order:
   - Start with `0_prompt_engineering.ipynb`
   - Continue to `1_multimodal_inputs.ipynb`
   - Explore the patterns in the `patterns/` directory

3. Each notebook contains:
   - Step-by-step explanations
   - Code examples that you can run
   - Progressive complexity to build your skills

## Central Utility Files

The repository includes centralized utility functions in `src/utils/bedrock_utils.py` to simplify working with the Bedrock API:

- `create_bedrock_client`: Create a Bedrock client
- `invoke_model`: Send requests to Bedrock models
- `extract_json_from_text`: Extract structured data from responses

## Learning Path

This repo will guide you through:

1. **Basic concepts**:
   - Prompt engineering fundamentals
   - Structured prompts and outputs
   - Working with multimodal inputs

2. **Advanced techniques**:
   - Response prefilling for structured outputs
   - Entity extraction
   - Chain of thought reasoning
   - Classification and routing

3. **Design patterns**:
   - Building robust GenAI applications
   - Implementing best practices
   - Creating complex workflows

## Contributing

Feel free to submit issues or pull requests to improve these examples!