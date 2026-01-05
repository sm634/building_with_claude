from anthropic import Anthropic
from dotenv import load_dotenv
from statistics import mean
import json
import os
# Functions to validate the output structure
import re
import ast

# iniitialize environment variables
_ = load_dotenv(override=True)
model = os.getenv("HAIKU_MODEL")
# model = os.getenv("CLAUDE_MODEL")

# initialize client
client = Anthropic()

# Initial prompt draft
def generate_answer_prompt(user_question):
    prompt = f"""
    Please answer the user's question:

    {user_question}
    """
    return prompt

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system_prompt=None, temperature=0.0, stop_sequences=None):
    """Chat with the math specialist model."""
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences
    }

    if system_prompt:
        params["system"] = system_prompt
    
    message = client.messages.create(**params)

    return message.content[0].text

# generate dataset using haiku model
def generate_dataset():
    prompt = """
    Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
    that generate Python, JSON, or Regex speficically for AWS-related tasks. Generate an array of Json objects,
    each representing task that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
        {
            "task": "Description of task",
            "format": "python" or "json" or "regex"
        },
        ...additional
    ]
    ```

    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single Regex pattern.
    * Focus on tasks that do not require writing much code.

    Please generate 3 objects.
    """
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])

    return json.loads(text)


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
    Please solve the following task: 
    {test_case['task']}

    * Respond only wiht Python, JSON, or plain Regex.
    * Do not add any comments or commentary or explanation
    """
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    answer = chat(messages, stop_sequences=["```"])
    return answer


#### Functions to validate output syntax

def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0


def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0


def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0


def grade_syntax(response, test_case):
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    elif format == "python":
        return validate_python(response)
    else:
        return validate_regex(response)

### EVAL WORKFLOW

def run_test_case(test_case):
    """Calls run_prompt, then rades the result"""
    output = run_prompt(test_case)

    # GRADING
    model_grade = grade_by_model(test_case, output)
    model_score = model_grade['score']
    reasoning = model_grade['reasoning']

    syntax_score = grade_syntax(output, test_case)

    # Total average score
    score = (model_score + syntax_score) / 2

    return {
        "output": output,
        "score": score,
        "test_case": test_case,
        "reasoning": reasoning
    }

def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = [run_test_case(test_case) for test_case in dataset]

    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")

    try:
        with open("eval_results.json", "w") as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"Error saving eval results: {e}")
    
    return results


############### GRADERS ############
##### Three different kinds.
# 1. Code, 2. Model, 3. Human
# Code grader - checks output length, verifies syntax and key words, readability scores.
# Model grader - uses another LLM to grade the output for response quality, quality of instruction following, completeness, helpfulness, safety.
# Human grader - Asks a human to assign a score to output. Useful for: general response quality, comprehensiveness, depth, conciseness, relevance.

## Evaluation Criteria
# 1. Format - code grader 
# 2. Valid Syntax - code grader
# 3. Task Following - model grader

# Function to grade a test case + output using a model
def grade_by_model(test_case, output):
    eval_prompt = f"""
    You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

    Original Task:
    <task>
    {test_case["task"]}
    </task>

    Solution to Evaluate:
    <solution>
    {output}
    </solution>

    Output Format
    Provide your evaluation as a structured JSON object with the following fields, in this specific order:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement
    - "reasoning": A concise explanation of your overall assessment
    - "score": A number between 1-10

    Respond with JSON. Keep your response concise and direct.
    Example response shape:
    {{
        "strengths": string[],
        "weaknesses": string[],
        "reasoning": string,
        "score": number
    }}
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])

    return json.loads(eval_text)




if __name__ == "__main__":

    try: 
        with open("generated_dataset.json", "r") as f:
            dataset = json.load(f)
    except FileNotFoundError:
        dataset = generate_dataset()

        with open("generated_dataset.json", "w") as f:
            json.dump(dataset, f, indent=2)

    results = run_eval(dataset)
