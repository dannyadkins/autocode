import openai
import os 

from dotenv import load_dotenv

load_dotenv()

openai.api_key=os.environ.get("OPENAI_API_KEY")

def get_completion(model: str, prompt: str):
    if (not model in ['gpt-3.5-turbo', 'gpt-4']):
        raise Exception("Invalid model: " + model)
    return openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])['choices'][0]['message']['content']

def summarize_commits(commits):
    pass 