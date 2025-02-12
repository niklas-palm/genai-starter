import os
import json
import base64
import re

def encode_file_to_base64(file_path):
    file_type = file_path.split(".")[-1]
    
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        return encoded_string.decode("utf-8"), file_type

def is_path_to_video(path):
    return os.path.isfile(path) and path.split(".")[-1] == "mp4"

def is_path_to_image(path):
    return os.path.isfile(path) and path.split(".")[-1].lower() in ("jpeg", "jpg", "png")

def get_prompt_payload(args, prefill=None):
    content = []

    for arg in args:
        if is_path_to_video(arg) or is_path_to_image(arg):
            KEY = "video" if is_path_to_video(arg) else "image"
            print(f"** {KEY} provided")
            encoded_file, file_type = encode_file_to_base64(arg)
            
            content.append(
                {
                    KEY: {
                        "format": file_type,
                        "source": {"bytes": encoded_file},
                    }
                }
              )
        else:
            content.append({"text": arg})

    messages = [
            {
                "role": "user",
                "content": content,
            }
        ]

    if prefill:
        print('** Prefilling the response')
        messages.append(
            {
                "role": "assistant",
                "content": [{"text": prefill}],
            }
        )

    prompt_config = {
        "inferenceConfig": {
            "temperature": 0
        },
        "messages": messages,
    }

    print('\n')
    return json.dumps(prompt_config)

def extract_and_load_json(text):
    match = re.search(r"```json\n(.*?)```", text, re.DOTALL)
    
    if not match:
        raise ValueError("No JSON object found in the string")
    
    json_str = match.group(1)
    
    try:
        json_obj = json.loads(json_str)
        return json_obj
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")