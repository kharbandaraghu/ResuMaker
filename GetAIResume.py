import argparse
import os
from Packages.AI import AIParser
import json

# Command line arguments
parser = argparse.ArgumentParser(description='AI Response')
parser.add_argument('-m','--model', type=str, default='GPT4', help='The AI model (default: GPT4)')
parser.add_argument('-t','--temperature', type=float, default=1, help='The temperature for AI response (default: 1)')
args = parser.parse_args()

# Get the absolute path of the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Text from custom base prompt
base_prompt_path = os.path.join(current_dir, 'Prompts/BasePrompt.txt')
with open(base_prompt_path, 'r') as f:
    base_prompt = f.read()

# Text from custom resume prompt
resume_prompt_path = os.path.join(current_dir, 'Prompts/CustomResumePrompt.txt')
with open(resume_prompt_path, 'r') as f:
    resume_prompt = f.read()

combined_prompt = base_prompt + resume_prompt

aiParser = AIParser(combined_prompt, MODEL=args.model)
response = aiParser.get_response(max_tokens=4000, temperature=args.temperature)
json_data = json.loads(response)

# Save AI response to resumeData.json
resume_data_path = os.path.join(current_dir, 'tmp/resumeData.json')
with open(resume_data_path, 'w+') as f:
    json.dump(json_data, f)

print("AI response saved to resumeData.json")
