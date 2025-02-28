import boto3
import os
import json
import base64
import re

# Common model IDs for easy reference
CLAUDE_3_5_SONNET = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
CLAUDE_3_5_HAIKU = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
NOVA_LITE = "us.amazon.nova-lite-v1:0"
NOVA_PRO = "us.amazon.nova-pro-v1:0"


def create_bedrock_client(region_name="us-west-2"):
    """
    Create a Bedrock client with the specified region.

    Args:
        region_name (str): AWS region name. Default is "us-west-2"

    Returns:
        boto3.client: Bedrock client
    """
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name,
    )


def text_completion(client, prompt, model_id=CLAUDE_3_5_SONNET, temperature=0):
    """
    Simple text completion with Bedrock models.

    Args:
        client: Bedrock client
        prompt (str): Text prompt to send
        model_id (str): Model ID to use
        temperature (float): Controls randomness (0-1)

    Returns:
        str: Model's text response
    """
    # Check if the model ID is for Nova
    # Use exact match as the model IDs include version numbers
    is_nova_model = "nova" in model_id.lower()

    # Format prompt according to model type
    if is_nova_model:
        # Nova models format - no "type" field needed
        body = json.dumps(
            {
                "inferenceConfig": {"temperature": temperature},
                "messages": [{"role": "user", "content": [{"text": prompt}]}],
            }
        )
    else:
        # Claude models format (all versions)
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": temperature,
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
            }
        )

    # Call the model
    response = client.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get("body").read())

    # Extract text based on model type
    if is_nova_model:
        # Nova models
        return response_body["output"]["message"]["content"][0]["text"]
    else:
        # Claude models (all versions)
        return response_body["content"][0]["text"]


def encode_image(file_path):
    """
    Encode an image file to base64 for API requests.

    Args:
        file_path (str): Path to the image file

    Returns:
        str: Base64 encoded image
    """
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def encode_video(file_path):
    """
    Encode a video file to base64 for API requests.

    Args:
        file_path (str): Path to the video file

    Returns:
        str: Base64 encoded video
    """
    with open(file_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")


def invoke_with_image(client, image_path, prompt, model_id=NOVA_LITE, temperature=0):
    """
    Invoke a model with an image and text.

    Args:
        client: Bedrock client
        image_path (str): Path to the image file
        prompt (str): Text prompt about the image
        model_id (str): Model ID to use (should support images)
        temperature (float): Controls randomness (0-1)

    Returns:
        str: Model's text response
    """
    # Get file extension
    file_type = image_path.split(".")[-1].lower()

    # Encode the image
    encoded_image = encode_image(image_path)

    # Check if the model ID is for Nova
    # Use exact match as the model IDs include version numbers
    is_nova_model = "nova" in model_id.lower()

    # Content with image and prompt
    if is_nova_model:
        # For Nova models, we need to format without the "type" field
        content = [
            {
                "image": {
                    "format": file_type,
                    "source": {"bytes": encoded_image},
                }
            },
            {"text": prompt},
        ]
    else:
        # For Claude models, include the type field
        content = [
            {
                "type": "image",
                "image": {
                    "format": file_type,
                    "source": {"bytes": encoded_image},
                },
            },
            {"type": "text", "text": prompt},
        ]

    # Create the request body based on model type
    if is_nova_model:
        body = json.dumps(
            {
                "inferenceConfig": {"temperature": temperature},
                "messages": [{"role": "user", "content": content}],
            }
        )
    else:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": temperature,
                "messages": [{"role": "user", "content": content}],
            }
        )

    # Call the model
    response = client.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get("body").read())

    # Return the text response based on model type
    if is_nova_model:
        # Nova models
        return response_body["output"]["message"]["content"][0]["text"]
    else:
        # Claude models
        return response_body["content"][0]["text"]


def invoke_with_video(client, video_path, prompt, model_id=NOVA_LITE, temperature=0):
    """
    Invoke a model with a video and text.

    Args:
        client: Bedrock client
        video_path (str): Path to the video file
        prompt (str): Text prompt about the video
        model_id (str): Model ID to use (should support videos)
        temperature (float): Controls randomness (0-1)

    Returns:
        str: Model's text response
    """
    # Get file extension
    file_type = video_path.split(".")[-1].lower()

    # Encode the video
    encoded_video = encode_video(video_path)

    # Check if the model ID is for Nova
    # Use exact match as the model IDs include version numbers
    is_nova_model = "nova" in model_id.lower()

    # Content with video and prompt
    if is_nova_model:
        # For Nova models, we need to format without the "type" field
        content = [
            {
                "video": {
                    "format": file_type,
                    "source": {"bytes": encoded_video},
                }
            },
            {"text": prompt},
        ]
    else:
        # For Claude models, include the type field
        content = [
            {
                "type": "video",
                "video": {
                    "format": file_type,
                    "source": {"bytes": encoded_video},
                },
            },
            {"type": "text", "text": prompt},
        ]

    # Create the request body based on model type
    if is_nova_model:
        body = json.dumps(
            {
                "inferenceConfig": {"temperature": temperature},
                "messages": [{"role": "user", "content": content}],
            }
        )
    else:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": temperature,
                "messages": [{"role": "user", "content": content}],
            }
        )

    # Call the model
    response = client.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get("body").read())

    # Return the text response based on model type
    if is_nova_model:
        # Nova models
        return response_body["output"]["message"]["content"][0]["text"]
    else:
        # Claude models
        return response_body["content"][0]["text"]


def extract_json_from_text(text):
    """
    Extract a JSON object from text within ```json blocks.

    Args:
        text (str): Text containing a JSON object

    Returns:
        dict: Extracted JSON object
    """
    # Look for JSON blocks
    match = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)

    if not match:
        # If no code blocks, try to find JSON-like content directly
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in the text")

    json_str = match.group(1) if match.group(1) else match.group(0)

    # Clean up the string
    json_str = json_str.strip()

    try:
        json_obj = json.loads(json_str)
        return json_obj
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


def invoke_with_prefill(
    client,
    prompt,
    prefill,
    model_id=NOVA_LITE,
    temperature=0,
    image_path=None,
    video_path=None,
):
    """
    Invoke a model with response prefilling. Can include image or video content.

    Args:
        client: Bedrock client
        prompt (str): Text prompt
        prefill (str): Text to start the model's response with
        model_id (str): Model ID to use
        temperature (float): Controls randomness (0-1)
        image_path (str, optional): Path to an image file to include with the prompt
        video_path (str, optional): Path to a video file to include with the prompt

    Returns:
        str: Model's completion (not including the prefill)
    """
    # Prepare user content list
    user_content = []

    # Add image if provided
    if image_path:
        file_type = image_path.split(".")[-1].lower()
        encoded_image = encode_image(image_path)
        user_content.append(
            {
                "type": "image",
                "image": {
                    "format": file_type,
                    "source": {"bytes": encoded_image},
                },
            }
        )

    # Add video if provided
    if video_path:
        file_type = video_path.split(".")[-1].lower()
        encoded_video = encode_video(video_path)
        user_content.append(
            {
                "type": "video",
                "video": {
                    "format": file_type,
                    "source": {"bytes": encoded_video},
                },
            }
        )

    # Add text prompt
    user_content.append({"type": "text", "text": prompt})

    # Ensure prefill doesn't have trailing whitespace
    prefill = prefill.rstrip()

    # Check if the model ID is for Nova
    # Use exact match as the model IDs include version numbers
    is_nova_model = "nova" in model_id.lower()

    # Create the request body based on model type
    if is_nova_model:
        # For Nova models, we need to format the content differently
        nova_user_content = []
        for item in user_content:
            if "type" in item:
                if item["type"] == "text":
                    nova_user_content.append({"text": item["text"]})
                elif item["type"] == "image":
                    nova_user_content.append({"image": item["image"]})
                elif item["type"] == "video":
                    nova_user_content.append({"video": item["video"]})

        body = json.dumps(
            {
                "inferenceConfig": {"temperature": temperature},
                "messages": [
                    {"role": "user", "content": nova_user_content},
                    {"role": "assistant", "content": [{"text": prefill}]},
                ],
            }
        )
    else:
        # Claude models
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": temperature,
                "messages": [
                    {"role": "user", "content": user_content},
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": prefill}],
                    },
                ],
            }
        )

    # Call the model
    response = client.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get("body").read())

    # Return just the completion (not including the prefill)
    if is_nova_model:
        # Nova models
        return response_body["output"]["message"]["content"][0]["text"]
    else:
        # Claude models
        return response_body["content"][0]["text"]
