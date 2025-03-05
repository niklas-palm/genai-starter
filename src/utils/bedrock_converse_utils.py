import boto3
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


def text_completion(client, prompt, model_id=NOVA_LITE, temperature=0):
    """
    Simple text completion with Bedrock models using the converse API.

    Args:
        client: Bedrock client
        prompt (str): Text prompt to send
        model_id (str): Model ID to use
        temperature (float): Controls randomness (0-1)

    Returns:
        str: Model's text response
    """
    # Create message object
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    # Call the model using converse API
    response = client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={"temperature": temperature},
    )

    # Extract the text response
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return content["text"]

    return ""


def read_file(file_path):
    """
    Read a file for API requests.

    Args:
        file_path (str): Path to the file

    Returns:
        bytes: File contents as bytes
    """
    with open(file_path, "rb") as file:
        return file.read()


def invoke_with_media(
    client, prompt, model_id=NOVA_LITE, temperature=0, image_path=None, video_path=None
):
    """
    Invoke a model with media (image or video) and text.

    Args:
        client: Bedrock client
        prompt (str): Text prompt about the media
        model_id (str): Model ID to use
        temperature (float): Controls randomness (0-1)
        image_path (str, optional): Path to an image file
        video_path (str, optional): Path to a video file

    Returns:
        str: Model's text response
    """
    # Build the content array starting with the text prompt
    content = [{"text": prompt}]

    # Add image if provided
    if image_path:
        file_type = image_path.split(".")[-1].lower()
        image_bytes = read_file(image_path)
        content.append(
            {"image": {"format": file_type, "source": {"bytes": image_bytes}}}
        )

    # Add video if provided
    if video_path:
        file_type = video_path.split(".")[-1].lower()
        video_bytes = read_file(video_path)
        content.append(
            {"video": {"format": file_type, "source": {"bytes": video_bytes}}}
        )

    # Create the message with media and text
    message = {
        "role": "user",
        "content": content,
    }

    # Call the model using converse API
    response = client.converse(
        modelId=model_id,
        messages=[message],
        inferenceConfig={"temperature": temperature},
    )

    # Extract the text response
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return content["text"]

    return ""


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


def generate_conversation(
    client,
    prompt,
    model_id=NOVA_LITE,
    temperature=0,
    system_prompt=None,
    conversation_history=None,
    image_path=None,
    video_path=None,
):
    """
    Generate a conversation using the Converse API, with optional media support.

    Args:
        client: Bedrock client
        prompt (str): Text prompt to send
        model_id (str): Model ID to use
        temperature (float): Controls randomness (0-1)
        system_prompt (str, optional): System prompt to guide the model's behavior
        conversation_history (list, optional): Previous messages in the conversation
        image_path (str, optional): Path to an image file to include with the prompt
        video_path (str, optional): Path to a video file to include with the prompt

    Returns:
        dict: Full response from the model, including the conversation
    """
    # Create messages array
    messages = conversation_history or []

    # Create content array for the current message
    content = [{"text": prompt}]

    # Add image if provided
    if image_path:
        file_type = image_path.split(".")[-1].lower()
        image_bytes = read_file(image_path)
        content.append(
            {"image": {"format": file_type, "source": {"bytes": image_bytes}}}
        )

    # Add video if provided
    if video_path:
        file_type = video_path.split(".")[-1].lower()
        video_bytes = read_file(video_path)
        content.append(
            {"video": {"format": file_type, "source": {"bytes": video_bytes}}}
        )

    # Add the current message
    messages.append({"role": "user", "content": content})

    # Create system prompts if provided
    system_prompts = None
    if system_prompt:
        system_prompts = [{"text": system_prompt}]

    # Call the model using converse API
    response = client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig={"temperature": temperature},
    )

    return response


def stream_conversation(
    client,
    prompt,
    model_id=NOVA_LITE,
    temperature=0,
    system_prompt=None,
    conversation_history=None,
    callback=None,
):
    """
    Stream a conversation using the Converse API.

    Args:
        client: Bedrock client
        prompt (str): Text prompt to send
        model_id (str): Model ID to use
        temperature (float): Controls randomness (0-1)
        system_prompt (str, optional): System prompt to guide the model's behavior
        conversation_history (list, optional): Previous messages in the conversation
        callback (callable, optional): Function to call with each streamed chunk

    Returns:
        str: Complete text response
    """
    # Create messages array
    messages = conversation_history or []

    # Add the current prompt
    messages.append({"role": "user", "content": [{"text": prompt}]})

    # Create system prompts if provided
    system_prompts = None
    if system_prompt:
        system_prompts = [{"text": system_prompt}]

    # Call the model using converse stream API
    response = client.converse_stream(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig={"temperature": temperature},
    )

    # Process the stream
    stream = response.get("stream")
    full_text = ""

    if stream:
        for event in stream:
            if "contentBlockDelta" in event:
                text_chunk = event["contentBlockDelta"]["delta"]["text"]
                full_text += text_chunk

                # Call the callback if provided
                if callback:
                    callback(text_chunk)

    return full_text


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
    content = [{"text": prompt}]

    # Add image if provided
    if image_path:
        file_type = image_path.split(".")[-1].lower()
        image_bytes = read_file(image_path)
        content.append(
            {"image": {"format": file_type, "source": {"bytes": image_bytes}}}
        )

    # Add video if provided
    if video_path:
        file_type = video_path.split(".")[-1].lower()
        video_bytes = read_file(video_path)
        content.append(
            {"video": {"format": file_type, "source": {"bytes": video_bytes}}}
        )

    # Create user message
    user_message = {"role": "user", "content": content}

    # Create assistant message with prefill
    assistant_message = {"role": "assistant", "content": [{"text": prefill}]}

    # Create messages array
    messages = [user_message, assistant_message]

    # Call the model using converse API
    response = client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={"temperature": temperature},
    )

    # Extract the text response (which will be the completion after the prefill)
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return content["text"]

    return ""
