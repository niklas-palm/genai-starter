import gradio as gr
import json
from example import classify_inquiry, technical_support_response, billing_inquiry_response, product_info_response, general_inquiry_response

def process_inquiry_with_steps(inquiry):
    # Step 1: Classification
    classification = classify_inquiry(inquiry)
    classification_output = f"Classification Results:\n{json.dumps(classification, indent=2)}"
    
    # Step 2: Routing and Response
    category = classification['category']
    language = classification['language']
    
    routing_info = f"Routing to: {category} handler in {language}"
    
    # Get response based on classification
    if category == 'Technical':
        response = technical_support_response(inquiry, language)
    elif category == 'Billing':
        response = billing_inquiry_response(inquiry, language)
    elif category == 'Product':
        response = product_info_response(inquiry, language)
    else:
        response = general_inquiry_response(inquiry, language)
    
    return classification_output, routing_info, response

iface = gr.Interface(
    fn=process_inquiry_with_steps,
    inputs=gr.Textbox(lines=3, label="Customer Inquiry"),
    outputs=[
        gr.Textbox(lines=5, label="Step 1: Classification"),
        gr.Textbox(lines=2, label="Step 2: Routing Decision"),
        gr.Textbox(lines=10, label="Step 3: Generated Response")
    ],
    title="Multi-lingual Customer Inquiry - Router Pattern",
    description="This example demonstrates the routing pattern using a multi-lingual customer inquiry system. Routing in the context of GenAI applications involves directing inputs to different models or processes based on certain criteria. This allows for more specialized and efficient handling of diverse inputs. See how your inquiry is classified, routed, and processed.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()