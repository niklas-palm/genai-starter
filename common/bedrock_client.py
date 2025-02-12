from common.utils import get_prompt_payload

import boto3
import json

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
)

MODEL_ID = "us.amazon.nova-lite-v1:0"
#MODEL_ID = "us.amazon.nova-pro-v1:0"

def invoke_model(*args, prefill=None):
    payload = get_prompt_payload(args, prefill=prefill)
    response = bedrock.invoke_model(
        body=payload,
        modelId=MODEL_ID,
    )

    return json.loads(response.get("body").read())

def get_completion_from_response(response):
    return response["output"]["message"]["content"][0]["text"]