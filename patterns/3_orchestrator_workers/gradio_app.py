import gradio as gr
from orchestrator import DocumentAnalysisOrchestrator
from extract_info_worker import extract_key_info
from identify_topics_worker import identify_topics
from summarize_methodology_worker import summarize_methodology
from highlight_findings_worker import highlight_key_findings
import json

EXAMPLE_PAPER = """Title: Advanced Machine Learning Techniques for Climate Change Prediction
Authors: John Smith, PhD; Maria Garcia, PhD; David Johnson, MSc
Abstract: This paper presents novel machine learning approaches for improving climate change predictions. We introduce a hybrid deep learning architecture that combines traditional climate models with neural networks to enhance the accuracy of long-term climate forecasts.

Methodology:
Our study employed a three-phase approach. First, we collected historical climate data from 1950-2020. Second, we developed a custom neural network architecture that processes both temporal and spatial climate patterns. Finally, we validated our model using held-out test data from recent years.

Key Findings:
1. The hybrid model showed a 23% improvement in prediction accuracy compared to traditional methods.
2. Neural networks were particularly effective at capturing non-linear climate patterns.
3. The model successfully predicted several extreme weather events in the validation period.

Discussion:
The results demonstrate the potential of machine learning in climate science, while also highlighting important limitations and areas for future research."""

class DocumentAnalysisWithLogging(DocumentAnalysisOrchestrator):
    def process_document(self, document):
        progress_log = "Starting document analysis...\n"
        
        futures = {
            'info': self.executor.submit(extract_key_info, document),
            'topics': self.executor.submit(identify_topics, document),
            'methodology': self.executor.submit(summarize_methodology, document),
            'findings': self.executor.submit(highlight_key_findings, document)
        }

        results = {}
        for key, future in futures.items():
            try:
                progress_log += f"\nProcessing {key}..."
                results[key] = future.result()
                progress_log += f"\nCompleted {key}"
            except Exception as e:
                progress_log += f"\nError in {key} task: {str(e)}"
                results[key] = None

        return progress_log, results

orchestrator = DocumentAnalysisWithLogging()

def process_document_with_steps(document):
    progress_log, results = orchestrator.process_document(document)
    formatted_results = json.dumps(results, indent=2)
    return progress_log, formatted_results

iface = gr.Interface(
    fn=process_document_with_steps,
    inputs=gr.Textbox(
        lines=10, 
        label="Scientific Paper Content",
        value=EXAMPLE_PAPER
    ),
    outputs=[
        gr.Textbox(lines=10, label="Processing Progress", elem_classes=["output-box"]),
        gr.Textbox(lines=20, label="Analysis Results", elem_classes=["output-box"])
    ],
    title="Multi-Stage Document Analysis - Orchestrator-Workers Pattern",
    description="This example demonstrates the orchestrator-workers pattern using a multi-stage document analysis system for scientific papers. The orchestrator-workers pattern involves a central coordinator (orchestrator) that manages and distributes tasks to multiple specialized workers. Each worker is responsible for a specific task, and the orchestrator handles the overall workflow and coordination.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()