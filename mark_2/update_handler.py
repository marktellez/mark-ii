import openai
import os

class UpdateHandler:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_update(self, issue_description, relevant_code):
        prompt = f"""
        Issue description: {issue_description}

        Relevant code files:
        {', '.join(relevant_code)}

        Please provide a detailed description of the necessary updates to address this issue,
        including any code changes, new files to be created, or modifications to existing files.
        Format your response as a markdown document with code blocks for each file that needs to be modified.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that helps with coding tasks."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                n=1,
                temperature=0.7,
            )

            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error generating update: {e}")
            return "Error: Unable to generate update description."
