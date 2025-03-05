import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import concurrent.futures
from src.utils import (
    create_bedrock_client,
    generate_conversation,
    NOVA_LITE
)

# Create a client once to be reused
bedrock_client = create_bedrock_client()

# System prompt for improved consistency across all interactions
SYSTEM_PROMPT = """
You are an AI assistant specializing in marketing content creation.
Create engaging, concise, and effective marketing content tailored for different platforms.
Focus on highlighting product benefits and value propositions.
"""

def generate_email_content(product_info):
    prompt = f"""
    Create engaging email marketing content for the following product.
    Include a catchy subject line and main body text.
    Keep it professional and focused on value proposition.
    
    Product Information:
    {product_info}
    
    Format the response as:
    Subject Line: [your subject line]
    ---
    [your email body]
    """
    response = generate_conversation(
        client=bedrock_client,
        prompt=prompt,
        model_id=NOVA_LITE,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Extract text from response
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return {"platform": "email", "content": content["text"]}
    
    return {"platform": "email", "content": "Error: No content generated"}

def generate_instagram_content(product_info):
    prompt = f"""
    Create engaging Instagram post content for the following product.
    Include:
    - Catchy caption (max 200 characters)
    - Relevant hashtags (max 5)
    - Key visual elements to include in the photo
    
    Product Information:
    {product_info}
    """
    response = generate_conversation(
        client=bedrock_client,
        prompt=prompt,
        model_id=NOVA_LITE,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Extract text from response
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return {"platform": "instagram", "content": content["text"]}
    
    return {"platform": "instagram", "content": "Error: No content generated"}

def generate_website_content(product_info):
    prompt = f"""
    Create engaging website product description content.
    Include:
    - Compelling headline
    - Product description (SEO-optimized)
    - Key features and benefits
    - Technical specifications
    
    Product Information:
    {product_info}
    """
    response = generate_conversation(
        client=bedrock_client,
        prompt=prompt,
        model_id=NOVA_LITE,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Extract text from response
    output_message = response["output"]["message"]
    for content in output_message["content"]:
        if "text" in content:
            return {"platform": "website", "content": content["text"]}
    
    return {"platform": "website", "content": "Error: No content generated"}

def generate_marketing_content_sequential(product_info):
    start_time = time.time()
    results = []
    
    print("Starting sequential content generation...\n")
    
    # Generate content for each platform sequentially
    email_content = generate_email_content(product_info)
    results.append(email_content)
    print(f"Email content generated: {email_content['content'][:100]}...\n")
    
    instagram_content = generate_instagram_content(product_info)
    results.append(instagram_content)
    print(f"Instagram content generated: {instagram_content['content'][:100]}...\n")
    
    website_content = generate_website_content(product_info)
    results.append(website_content)
    print(f"Website content generated: {website_content['content'][:100]}...\n")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return results, execution_time

def generate_marketing_content_parallel(product_info):
    start_time = time.time()
    results = []
    
    print("Starting parallel content generation...\n")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create tasks for each platform
        tasks = {
            executor.submit(generate_email_content, product_info): "email",
            executor.submit(generate_instagram_content, product_info): "instagram",
            executor.submit(generate_website_content, product_info): "website"
        }
        
        for future in concurrent.futures.as_completed(tasks):
            platform = tasks[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Generated content for {platform}: {result['content'][:100]}...\n")
            except Exception as exc:
                print(f"{platform} content generation failed: {exc}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return results, execution_time

# Example usage
if __name__ == "__main__":
    product_info = """
    Product: EcoTech Smart Water Bottle
    Price: $39.99
    Features:
    - Temperature monitoring and display
    - Hydration tracking with smartphone app
    - LED reminder system
    - 24-hour temperature retention
    - 750ml capacity
    - Made from recycled stainless steel
    - Available in: Ocean Blue, Forest Green, Sunset Orange
    
    Key Benefits:
    - Helps maintain optimal hydration
    - Eco-friendly materials
    - Smart technology integration
    - Premium build quality
    """

    # Run sequential execution
    sequential_results, sequential_time = generate_marketing_content_sequential(product_info)
    print(f"\nSequential execution completed in {sequential_time:.2f} seconds")

    print("\n" + "="*50 + "\n")

    # Run parallel execution
    parallel_results, parallel_time = generate_marketing_content_parallel(product_info)
    print(f"\nParallel execution completed in {parallel_time:.2f} seconds")

    # Calculate and display the performance improvement
    improvement = (sequential_time - parallel_time) / sequential_time * 100
    print(f"\nPerformance improvement: {improvement:.1f}%")