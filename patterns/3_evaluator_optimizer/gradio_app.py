import gradio as gr
import json
from example import SubjectLineGenerator, SubjectLineEvaluator, SubjectLineOptimizer

EXAMPLE_EMAIL = """We're excited to announce the launch of our new product line, EcoClean. 
These environmentally friendly cleaning products are just as effective as traditional cleaners 
but are made from 100% biodegradable ingredients. For the next week, we're offering a 20% discount 
on all EcoClean products to our loyal customers. Don't miss this chance to make your home cleaner 
and greener!"""


def optimize_subject_line(email_content, num_iterations):
    generator = SubjectLineGenerator()
    evaluator = SubjectLineEvaluator()
    optimizer = SubjectLineOptimizer(generator, evaluator)

    progress_output = ""

    def capture_print(text):
        nonlocal progress_output
        progress_output += text + "\n"

    # Temporarily redirect print statements to our capture function
    import builtins

    original_print = builtins.print
    builtins.print = capture_print

    try:
        best_subject, best_score = optimizer.optimize(
            email_content, iterations=num_iterations
        )

        final_output = f"""
Best Subject Line: {best_subject}
Best Score: {best_score}
"""
    finally:
        # Restore original print function
        builtins.print = original_print

    return progress_output, final_output


iface = gr.Interface(
    fn=optimize_subject_line,
    inputs=[
        gr.Textbox(lines=6, label="Email Content", value=EXAMPLE_EMAIL),
        gr.Slider(minimum=1, maximum=5, step=1, value=3, label="Number of Iterations"),
    ],
    outputs=[
        gr.Textbox(
            lines=20, label="Optimization Progress", elem_classes=["output-box"]
        ),
        gr.Textbox(lines=3, label="Final Result", elem_classes=["output-box"]),
    ],
    title="Email Subject Line Optimizer - Evaluator-Optimizer Pattern",
    description=" This example demonstrates the evaluator-optimizer pattern using an automated email subject line generator for marketing campaigns. The evaluator-optimizer pattern involves generating multiple outputs, evaluating their quality based on specific criteria, and then using that evaluation to inform and improve future generations. This creates a feedback loop that can lead to increasingly better results. Watch as the system generates, evaluates, and optimizes email subject lines through multiple iterations.",
    allow_flagging="never",
)

if __name__ == "__main__":
    iface.launch()
