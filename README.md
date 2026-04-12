# AI Role Certification Service

## Overview

This project provides an AI-driven approach to access reviews and role certification using structured question-and-answer data to determine appropriate role assignments.

It leverages the OpenAI Responses API with prompt templates to analyse user responsibilities and map them to predefined roles.

---

## Features

- AI-powered role assignment based on user responsibilities
- Structured input using JSON question/answer sets
- Prompt templating via OpenAI hosted prompts
- Modular service design for easy extension
- Test data included for rapid iteration

---

## Project Structure

.
│ .env
│ main.py
│ requirements.txt
│
├── services
│ ai_prompts.py
│
├── testdata
│ question_answer_sets.json
│ example_response_1.json



---

## Setup

### 1. Clone the repository

git clone <your-repo-url>  
cd ai_certification

---

### 2. Create a virtual environment

python -m venv environments/ai_certification  

Windows:
environments\ai_certification\Scripts\activate  

Linux/macOS:
source environments/ai_certification/bin/activate  

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Configure environment variables

Create a `.env` file:

OPENAI_API_KEY=your_api_key_here  
ROLE_ASSIGNMENT_PROMPT_ID=your_prompt_id  

---

## How It Works

1. Input Data  
   A JSON file (`question_answer_sets.json`) contains user responses to role-related questions.

2. Data Loading  
   The service loads this file into a Python dictionary using `pathlib`.

3. Prompt Execution  
   Data is passed into an OpenAI stored prompt using the Responses API.

4. AI Evaluation  
   The model evaluates answers and determines role assignments.

5. Output  
   The system returns structured role recommendations.

---

## Input Format

Example `question_answer_sets.json`:

```json
[
  {
    "id": "Q1",
    "text": "Describe your responsibilities",
    "answer": "I manage user access and permissions"
  }
]

# Sending Data to OpenAI

Important: OpenAI prompt variables do NOT accept raw JSON arrays or objects directly.

## Correct approach

import json

user_question_answers = {{
"type": "input_text",
"text": json.dumps(questionData)
}}

---

# Running the Project

Run directly:

python -m services.ai_prompts

Or with FastAPI:

uvicorn main:app --reload

---

# Testing

Test data is located at:

testdata/question_answer_sets.json

Modify this file to simulate different user profiles and access scenarios.

---

# Common Pitfalls

## 1. Passing arrays directly to OpenAI

Not allowed  
Always serialize using json.dumps()

## 2. Incorrect variable types

Using type = "json" is not allowed  
Must use type = "input_text"

---

# Use Case: Access Certification

This project supports:

Identity and Access Management (IAM)  
Role-based access control (RBAC) reviews  
Compliance audits  
Periodic access certification  

---

# Future Improvements

Pydantic schema validation  
Role confidence scoring  
Audit logging  
Web UI dashboard  
Batch processing for large organisations  

---

# Contributing

You can extend the system by improving:

Prompt design  
Role mapping logic  
Input schemas  
Evaluation rules  

---

# License

MIT (or your chosen license)

---

# Summary

This system demonstrates how AI can:

Interpret user responsibilities  
Standardise access decisions  
Reduce manual review effort  
Improve consistency in role assignment

## Running

uvicorn main:app --host 0.0.0.0 --port 8000 --reload