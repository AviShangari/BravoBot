import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

class LLMInterface:
    def __init__(self, model="llama3.2"):
        load_dotenv()
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def ask(self, prompt):
        """
        Send a plain prompt to the model and return the response.
        """
        return self._call_ollama(prompt)
    
    def _call_ollama(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['response'].strip()
        except Exception as e:
            print(f"Error talking to Ollama: {e}")
            return "Sorry, I couldn't process that."
        
    def ask_with_openai(self, prompt):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("OpenAI error:", e)
            return "Sorry, I couldn't get a response from GPT."

# Example usage:
if __name__ == "__main__":
    llm = LLMInterface()
    print("Intent Response:", llm.detect_intent("Can you search for worm tracking techniques?"))
    print("Chat Response:", llm.ask("What is a transformer in machine learning?"))
