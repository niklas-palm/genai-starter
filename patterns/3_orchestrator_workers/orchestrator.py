import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import concurrent.futures
from extract_info_worker import extract_key_info
from identify_topics_worker import identify_topics
from summarize_methodology_worker import summarize_methodology
from highlight_findings_worker import highlight_key_findings

class DocumentAnalysisOrchestrator:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def process_document(self, document):
        futures = {
            'info': self.executor.submit(extract_key_info, document),
            'topics': self.executor.submit(identify_topics, document),
            'methodology': self.executor.submit(summarize_methodology, document),
            'findings': self.executor.submit(highlight_key_findings, document)
        }

        results = {}
        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:
                print(f"Error in {key} task: {str(e)}")
                results[key] = None

        return results

    def shutdown(self):
        self.executor.shutdown()

# Example usage
if __name__ == "__main__":
    orchestrator = DocumentAnalysisOrchestrator()

    sample_documents = [
        "Title: Advanced ML Techniques\nAuthors: John Doe, Jane Smith\nAbstract: This paper explores...\nMethodology: We used a novel approach...\nFindings: Our results show significant improvements...",
        "Title: Climate Change Effects\nAuthors: Alice Johnson\nAbstract: This study investigates...\nMethodology: A longitudinal study was conducted...\nFindings: The data indicates a strong correlation..."
    ]

    for i, doc in enumerate(sample_documents):
        print(f"\nProcessing document {i+1}:")
        results = orchestrator.process_document(doc)
        for key, value in results.items():
            print(f"{key.capitalize()}:")
            print(value)
            print()

    orchestrator.shutdown()