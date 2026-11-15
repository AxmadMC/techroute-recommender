# Agentic Workflow Traces

- Command: `python scripts/generate_agent_traces.py`
- Date: 2026-11-15
- Model: `gemini-3.1-flash-lite`

Each fenced block contains the in-memory trace returned by a real Gemini-backed run; no API key or full profile is included.

## ai_engineering_student

```json
[
  {
    "step_name": "PLAN",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "Created a plan for 4 retrieved opportunities.",
    "plan": [
      {
        "title": "AI Engineer",
        "stage": "Foundations",
        "reason": "It provides a structured roadmap to align with your target track as a beginner."
      },
      {
        "title": "Kaggle Learn Python Pandas and Intro to Machine Learning",
        "stage": "Foundations",
        "reason": "This course builds essential Python and machine learning basics through a preferred free and remote format."
      },
      {
        "title": "Data Analysis with Python",
        "stage": "Build Skills",
        "reason": "This certification allows for deep technical skill development in your primary interest area."
      },
      {
        "title": "Titanic competition",
        "stage": "Prove Skills",
        "reason": "This project offers a practical, competition-based environment to test data analysis skills."
      }
    ]
  },
  {
    "step_name": "GENERATE",
    "attempt_number": 1,
    "decision": "draft_received",
    "verifier_errors": [],
    "detail": "Received the initial path draft."
  },
  {
    "step_name": "VERIFY",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "Valid JSON, retrieved titles, stage order, uniqueness, and stage-size limits passed."
  },
  {
    "step_name": "DECIDE",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "AI-generated path accepted after 0 self-correction(s).",
    "repair_attempts": 0
  }
]
```

## cloud_career_changer

```json
[
  {
    "step_name": "PLAN",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "Created a plan for 4 retrieved opportunities.",
    "plan": [
      {
        "title": "AZ-900 learning paths",
        "stage": "Foundations",
        "reason": "This resource provides a self-paced, free introduction to Azure cloud concepts that aligns with your specific interests."
      },
      {
        "title": "AWS Educate",
        "stage": "Build Skills",
        "reason": "This program offers hands-on, self-paced learning to deepen your foundational cloud knowledge."
      },
      {
        "title": "Home lab: static site on AWS or Azure free tier",
        "stage": "Prove Skills",
        "reason": "Building a project allows you to apply your theoretical knowledge to a practical, remote-friendly scenario within your time constraints."
      },
      {
        "title": "Cloud Engineering",
        "stage": "Apply",
        "reason": "This program provides a structured pathway to further develop skills and prepare for professional opportunities in cloud computing."
      }
    ]
  },
  {
    "step_name": "GENERATE",
    "attempt_number": 1,
    "decision": "draft_received",
    "verifier_errors": [],
    "detail": "Received the initial path draft."
  },
  {
    "step_name": "VERIFY",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "Valid JSON, retrieved titles, stage order, uniqueness, and stage-size limits passed."
  },
  {
    "step_name": "DECIDE",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "AI-generated path accepted after 0 self-correction(s).",
    "repair_attempts": 0
  }
]
```

## software_engineering_student

```json
[
  {
    "step_name": "PLAN",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "Created a plan for 8 retrieved opportunities.",
    "plan": [
      {
        "title": "CS50P",
        "stage": "Foundations",
        "reason": "This course provides a comprehensive, self-paced introduction to Python matching your core interest."
      },
      {
        "title": "GitHub Skills courses",
        "stage": "Foundations",
        "reason": "These courses offer a self-paced way to learn Git, which is a required skill for your track."
      },
      {
        "title": "CS50x",
        "stage": "Build Skills",
        "reason": "This broad computer science curriculum builds the necessary software engineering depth for your learning path."
      },
      {
        "title": "CS50x final project",
        "stage": "Build Skills",
        "reason": "This project allows you to apply learned concepts in a self-paced format while respecting your time constraints."
      },
      {
        "title": "GitHub Student Developer Pack",
        "stage": "Build Skills",
        "reason": "Accessing these tools will provide a professional environment for your development needs."
      },
      {
        "title": "Open source contributions with good first issues",
        "stage": "Prove Skills",
        "reason": "Engaging in open source is a practical way to demonstrate your Git and Python proficiency to others."
      },
      {
        "title": "Outreachy internships",
        "stage": "Apply",
        "reason": "This remote internship opportunity allows you to gain real-world software engineering experience."
      },
      {
        "title": "MLH Fellowship",
        "stage": "Apply",
        "reason": "This remote fellowship provides structured, professional experience to transition you into a software engineering career."
      }
    ]
  },
  {
    "step_name": "GENERATE",
    "attempt_number": 1,
    "decision": "draft_received",
    "verifier_errors": [],
    "detail": "Received the initial path draft."
  },
  {
    "step_name": "VERIFY",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "Valid JSON, retrieved titles, stage order, uniqueness, and stage-size limits passed."
  },
  {
    "step_name": "DECIDE",
    "attempt_number": 1,
    "decision": "accepted",
    "verifier_errors": [],
    "detail": "AI-generated path accepted after 0 self-correction(s).",
    "repair_attempts": 0
  }
]
```
