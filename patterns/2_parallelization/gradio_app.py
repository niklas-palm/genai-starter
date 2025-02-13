import gradio as gr
from example import (
    generate_marketing_content_sequential,
    generate_marketing_content_parallel
)
import time

EXAMPLE_PRODUCT = """Product: EcoTech Smart Water Bottle
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
- Premium build quality"""

def process_product_info(product_info, execution_mode):
    progress_output = ""
    
    if execution_mode == "Compare Both":
        # Run sequential first
        progress_output += "Running sequential execution...\n"
        sequential_results, sequential_time = generate_marketing_content_sequential(product_info)
        sequential_content = {result['platform']: result['content'] for result in sequential_results}
        
        progress_output += f"Sequential execution completed in {sequential_time:.2f} seconds\n\n"
        
        # Run parallel
        progress_output += "Running parallel execution...\n"
        parallel_results, parallel_time = generate_marketing_content_parallel(product_info)
        parallel_content = {result['platform']: result['content'] for result in parallel_results}
        
        progress_output += f"Parallel execution completed in {parallel_time:.2f} seconds\n"
        
        # Calculate improvement
        improvement = (sequential_time - parallel_time) / sequential_time * 100
        progress_output += f"\nPerformance improvement with parallelization: {improvement:.1f}%"
        
        content = parallel_content  # Use parallel results for display
    
    else:
        # Run single mode (either sequential or parallel)
        if execution_mode == "Sequential":
            results, exec_time = generate_marketing_content_sequential(product_info)
        else:  # Parallel
            results, exec_time = generate_marketing_content_parallel(product_info)
            
        content = {result['platform']: result['content'] for result in results}
        progress_output += f"{execution_mode} execution completed in {exec_time:.2f} seconds"
    
    return (
        progress_output,
        content.get('email', 'Error generating email content'),
        content.get('instagram', 'Error generating Instagram content'),
        content.get('website', 'Error generating website content')
    )

iface = gr.Interface(
    fn=process_product_info,
    inputs=[
        gr.Textbox(
            lines=15, 
            label="Product Information", 
            value=EXAMPLE_PRODUCT
        ),
        gr.Radio(
            choices=["Sequential", "Parallel", "Compare Both"],
            label="Execution Mode",
            value="Compare Both"
        )
    ],
    outputs=[
        gr.Textbox(lines=6, label="Processing Progress and Performance Metrics"),
        gr.Textbox(lines=10, label="Email Marketing Content"),
        gr.Textbox(lines=10, label="Instagram Content"),
        gr.Textbox(lines=15, label="Website Content")
    ],
    title="Marketing Content Generator - Parallelization Pattern",
    description="""Parallelization in GenAI applications involves processing multiple inputs simultaneously using multiple threads or processes. This can significantly reduce the overall processing time for large numbers of similar tasks. 
    
    This example demonstrates the parallelization pattern by generating marketing content for multiple platforms.
    You can compare sequential vs parallel execution to see the performance benefits of parallelization.
    - Sequential: Generates content for each platform one after another
    - Parallel: Generates content for all platforms simultaneously
    - Compare Both: Runs both methods and shows the performance improvement""",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()