# TechRoute Sample Runs
Date: 2026-11-14
Model: `gemini-3.1-flash-lite`

## a) Cloud career changer (Gemini path)
Command: `python -m src.main --profile cloud_career_changer`
Input profile: {
  "target_track": "cloud_computing",
  "preferred_format": "self_paced",
  "skill_level": 0.3,
  "prefers_free": true,
  "needs_remote": true,
  "max_hours": 10,
  "interests": [
    "azure",
    "cloud",
    "linux"
  ]
}

```text
Loading opportunities from data/opportunities.csv...

Top opportunities:

AZ-900 learning paths - Score: 5.57
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)

AWS Cloud Practitioner Essentials - Score: 5.40
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)

AWS Educate - Score: 5.40
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)

Home lab: static site on AWS or Azure free tier - Score: 5.17
Because: career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)

Azure Fundamentals AZ-900 - Score: 5.07
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)

Privacy notice: only learning preferences (no personal data) and retrieved opportunity details are sent to Gemini.

Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Gain a broad understanding of cloud computing terminology and concepts.
   Opportunities: AZ-900 learning paths, AWS Cloud Practitioner Essentials
   Why: These resources establish the necessary baseline knowledge of cloud architecture and services required for beginners.
2. Build Skills: Develop hands-on experience and structured cloud engineering knowledge.
   Opportunities: AWS Educate, Cloud Engineering
   Why: Engaging with structured programs provides practical guided learning environments to deepen technical competencies.
3. Prove Skills: Validate your cloud proficiency through industry-recognized certification and practical application.
   Opportunities: Home lab: static site on AWS or Azure free tier, Azure Fundamentals AZ-900, AWS Certified Cloud Practitioner
   Why: Testing your knowledge through formal certification and applying it to a personal project proves capability to prospective environments.
4. Apply: Transition from learning to active professional roles.
   Why: No internship or job opportunities are in the dataset yet.
```

## b) AI Engineering student (Gemini path)
Command: `python -m src.main --profile ai_engineering_student`
Input profile: {
  "target_track": "ai_engineering",
  "preferred_format": "project_based",
  "skill_level": 0.35,
  "prefers_free": true,
  "needs_remote": true,
  "max_hours": 12,
  "interests": [
    "python",
    "machine_learning",
    "data_analysis"
  ]
}

```text
Loading opportunities from data/opportunities.csv...

Top opportunities:

Titanic competition - Score: 6.45
Because: career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.50)

Applied AI app with local model - Score: 5.92
Because: career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.30); interest overlap (+0.17)

Data Analysis with Python - Score: 5.80
Because: career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.02); interest overlap (+0.33)

Machine Learning with Python - Score: 5.80
Because: career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.02); interest overlap (+0.33)

CS50 AI - Score: 4.78
Because: career track match (+2.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)

Privacy notice: only learning preferences (no personal data) and retrieved opportunity details are sent to Gemini.

Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Gain a structured overview of the AI engineering field and establish programming basics.
   Opportunities: AI Engineer, Kaggle Learn Python Pandas and Intro to Machine Learning
   Why: Establishing a foundational understanding of the roadmap and essential Python libraries is necessary before beginning complex projects.
2. Build Skills: Develop core proficiencies in data analysis and machine learning concepts through structured learning.
   Opportunities: Data Analysis with Python, Machine Learning with Python, AI Engineering, CS50 AI
   Why: These programs provide the theoretical depth and technical competency required for AI engineering roles.
3. Prove Skills: Demonstrate knowledge through hands-on practice and application of machine learning techniques.
   Opportunities: Titanic competition, Applied AI app with local model
   Why: Applying learned concepts to real datasets and model deployment validates your technical capabilities and builds a project portfolio.
4. Apply: Transition to professional practice and gain real-world experience.
   Why: No internship or job opportunities are in the dataset yet.
```

## c) Cybersecurity beginner (offline fallback)
Command: `python -m src.main --profile cybersecurity_beginner --offline`
Input profile: {
  "target_track": "cybersecurity",
  "preferred_format": "self_paced",
  "skill_level": 0.2,
  "prefers_free": true,
  "needs_remote": true,
  "max_hours": 5,
  "interests": [
    "security_fundamentals",
    "linux",
    "networking"
  ]
}

```text
2026-11-14 22:38:38 WARNING gemini_call_skipped reason=no API key
Loading opportunities from data/opportunities.csv...

Top opportunities:

CS50 Cybersecurity - Score: 5.57
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)

Introduction to Cybersecurity - Score: 5.57
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)

Junior Cybersecurity Analyst career path - Score: 5.57
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)

CompTIA Security+ videos - Score: 5.57
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)

Cyber Security 101 - Score: 5.50
Because: career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.50)

Privacy notice: only learning preferences (no personal data) are used; offline mode sends no data to Gemini.

Generated learning path - Source: rule-based fallback (reason: offline mode):

1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: Introduction to Cybersecurity, Pre Security, Cyber Security 101, CS50 Cybersecurity, CompTIA Security+ videos, Junior Cybersecurity Analyst career path
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Why: These retrieved resources provide practical tool or lab experience.
3. Prove Skills: Demonstrate skills with retrieved projects and credentials.
   Opportunities: OverTheWire Bandit, Security Compliance and Identity Fundamentals SC-900
   Why: Projects, certifications, and contributions can demonstrate progress.
4. Apply: No internship or job opportunities are in the dataset yet for this track.
   Why: No matching internship or job rows were retrieved.
```

## d) Unknown profile (guardrail)
Command: `python -m src.main --profile not_a_real_profile`
Input profile: Profile name: not_a_real_profile (no matching preset)

```text
Error: unknown profile 'not_a_real_profile'. Valid profile names: it_support_beginner, networking_student, cybersecurity_beginner, cloud_career_changer, ai_engineering_student, software_engineering_student
```
