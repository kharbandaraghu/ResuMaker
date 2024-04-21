import os
from dotenv import load_dotenv
from openai import OpenAI
# Get current directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Specify path for .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(current_directory)), '.env')
MODELS={
    "GPT3": "gpt-3.5-turbo-0125",
    "GPT4":"gpt-4-0125-preview",
    "GPT4_OLD": "gpt-4-1106-preview"
}


class AIParser:
    def __init__(self, PROMPT, MODEL="GPT3"):
        self.prompt = PROMPT
        self.client = OpenAI()
        self.client.api_key = os.getenv("OPENAI_API_KEY")
        # map model to variables using dictionary
        self.model = MODELS[MODEL]
        #if not found throw error
        if self.model is None:
            raise ValueError("Model not found")

    def get_response(self, max_tokens=4000, temperature=1.0, frequency_penalty=0.0):
        

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": self.prompt} 
            ],
            response_format={ "type": "json_object" },
            stream=True,
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=frequency_penalty
        )
        resp = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end='')   
                resp += chunk.choices[0].delta.content
        print()
        return resp
