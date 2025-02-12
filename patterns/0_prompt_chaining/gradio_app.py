import gradio as gr
import json
from example import analyze_inquiry, generate_response_points, craft_email

EXAMPLE_INQUIRY = """I've been waiting for my order #12345 for over a week now, and it still hasn't arrived. 
This is unacceptable! I paid for express shipping and was promised delivery within 3 days. 
Can you tell me where my package is and why it's taking so long? I need this for an important event this weekend."""

def generate_email_with_steps(inquiry):
    # Step 1: Analyze inquiry
    analysis = analyze_inquiry(inquiry)
    analysis_output = f"Step 1 - Analysis:\n{json.dumps(analysis, indent=2)}\n\n"
    
    # Step 2: Generate response points
    points = generate_response_points(analysis)
    points_output = f"Step 2 - Response Points:\n{json.dumps(points, indent=2)}\n\n"
    
    # Step 3: Craft email
    email = craft_email(analysis, points)
    email_output = f"Step 3 - Final Email:\n{email}"
    
    return analysis_output, points_output, email_output

iface = gr.Interface(
    fn=generate_email_with_steps,
    inputs=gr.Textbox(
        lines=5, 
        label="Customer Inquiry",
        value=EXAMPLE_INQUIRY,  # Pre-filled value
        placeholder="Enter a customer inquiry here..."
    ),
    outputs=[
        gr.Textbox(lines=5, label="Step 1: Inquiry Analysis", elem_classes=["output-box"]),
        gr.Textbox(lines=5, label="Step 2: Response Points", elem_classes=["output-box"]),
        gr.Textbox(lines=10, label="Step 3: Generated Email", elem_classes=["output-box"])
    ],
    title="Customer Support Email Generator - Prompt Chaining Pattern",
    description="This example demonstrates the prompt chaining pattern using a customer support email generator. Prompt chaining is a technique where the output of one prompt is used as input for the next prompt in a sequence. This allows for more complex tasks to be broken down into smaller, manageable steps, each building upon the previous one. See how each step in the prompt chain processes your customer inquiry.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()