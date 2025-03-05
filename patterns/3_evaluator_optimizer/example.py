import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils import (
    create_bedrock_client,
    generate_conversation,
    extract_json_from_text,
    invoke_with_prefill,
    NOVA_LITE
)

# Create a client once to be reused
bedrock_client = create_bedrock_client()

# System prompt for better consistency 
SYSTEM_PROMPT = """
You are an AI assistant helping with email marketing optimization.
When asked for JSON output, always format properly within ```json code blocks.
Focus on creating compelling, concise, and effective email subject lines.
"""

class SubjectLineGenerator:
    def generate(self, email_content, num_options=5):
        prompt = f"""
        Generate {num_options} engaging email subject lines for the following email content. 
        Each subject line should be unique and compelling.
        Return the result as a JSON array of strings.

        Email content:
        {email_content}
        """
        # Using prefill to ensure proper JSON structure
        prefill = """```json
[
  """
        
        result = invoke_with_prefill(
            client=bedrock_client,
            prompt=prompt,
            prefill=prefill,
            model_id=NOVA_LITE,
        )
        
        # Combine prefill with result
        full_result = prefill + result
        return extract_json_from_text(full_result)

class SubjectLineEvaluator:
    def evaluate(self, subject_line, email_content):
        prompt = f"""
        Evaluate the following email subject line based on these criteria:
        1. Relevance to content (0-10)
        2. Catchiness (0-10)
        3. Clarity (0-10)
        4. Urgency (0-10)

        Subject line: "{subject_line}"
        Email content: "{email_content}"

        Return the result as a JSON object with keys 'relevance', 'catchiness', 'clarity', 'urgency', and 'total_score'.
        The 'total_score' should be the sum of all other scores.
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
                return extract_json_from_text(content["text"])
        
        return {"total_score": 0}  # Default in case of failure

class SubjectLineOptimizer:
    def __init__(self, generator, evaluator):
        self.generator = generator
        self.evaluator = evaluator

    def optimize(self, email_content, iterations=3, options_per_iteration=5):
        best_subject_line = ""
        best_score = 0

        for i in range(iterations):
            print(f"\nIteration {i+1}:")
            subject_lines = self.generator.generate(email_content, options_per_iteration)
            
            for subject_line in subject_lines:
                evaluation = self.evaluator.evaluate(subject_line, email_content)
                print(f"Subject Line: {subject_line}")
                print(f"Score: {evaluation['total_score']}")
                
                if evaluation['total_score'] > best_score:
                    best_subject_line = subject_line
                    best_score = evaluation['total_score']

            # Feedback for next iteration
            if i < iterations - 1:  # Don't need feedback after the last iteration
                feedback_prompt = f"""
                Based on the best subject line so far: "{best_subject_line}" with score {best_score},
                provide brief feedback on how to improve for the next iteration.
                """
                
                response = generate_conversation(
                    client=bedrock_client,
                    prompt=feedback_prompt,
                    model_id=NOVA_LITE,
                    system_prompt=SYSTEM_PROMPT
                )
                
                # Extract text from response
                output_message = response["output"]["message"]
                for content in output_message["content"]:
                    if "text" in content:
                        feedback = content["text"]
                
                print(f"\nFeedback for next iteration: {feedback}")
                
                # Update email_content with feedback for next iteration
                email_content += f"\nImprovement feedback: {feedback}"
        
        return best_subject_line, best_score

# Example usage
if __name__ == "__main__":
    generator = SubjectLineGenerator()
    evaluator = SubjectLineEvaluator()
    optimizer = SubjectLineOptimizer(generator, evaluator)

    email_content = """
    We're excited to announce the launch of our new product line, EcoClean. 
    These environmentally friendly cleaning products are just as effective as traditional cleaners 
    but are made from 100% biodegradable ingredients. For the next week, we're offering a 20% discount 
    on all EcoClean products to our loyal customers. Don't miss this chance to make your home cleaner 
    and greener!
    """

    best_subject, best_score = optimizer.optimize(email_content)

    print("\nOptimization complete!")
    print(f"Best Subject Line: {best_subject}")
    print(f"Best Score: {best_score}")