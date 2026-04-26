import json
from backend.utils import call_llm
import ast

def safe_parse_list(text):
    try:
        return ast.literal_eval(text)
    except:
        return []
    

def extract_skills(text):
    text = text[:1000]
    prompt = f"""
    Extract ONLY skills from the text below.

    Rules:
    - Return a Python list
    - No explanation

    Text:
    {text}
    """
    res = call_llm(prompt, 300)
    return safe_parse_list(res)


def generate_questions(skill):
    prompt = f"""
    Generate 3 interview questions for {skill}:

    Return STRICT JSON:
{{
  "basic": "...",
  "intermediate": "...",
  "advanced": "..."
}}


    Keep concise.
    """
    return call_llm(prompt, 300)


def evaluate_answer(skill, answer):
    prompt = f"""
    Evaluate answer for {skill}.

    Return STRICT JSON:
    {{
        "score": number (0-10),
        "feedback": "short feedback"
    }}

    Answer:
    {answer}
    """
    return call_llm(prompt, 300)


def generate_learning_plan(gaps):
    
    if not gaps:
        return "No major skill gaps identified. Focus on advanced projects."

    prompt = f"""
You are a career coach.

Create a clean 3-week learning roadmap.

Skills to improve:
{gaps}

Requirements:
- Include time estimate for each week (in hours)
- Include only high-quality curated resources (YouTube, docs, courses)
- Keep it practical and realistic
- DO NOT include mini projects
- Do NOT ask questions

Format:

Week 1:
Topics:
- ...

Time Required:
- ~X hours

Resources:
- ...

Week 2:
Topics:
- ...

Time Required:
- ~X hours

Resources:
- ...

Week 3:
Topics:
- ...

Time Required:
- ~X hours

Resources:s
- ...
"""

    response = call_llm(prompt, max_tokens=800)

    
    if not response or len(response.strip()) < 10:
        return "Learning plan could not be generated. Try again."

    return response