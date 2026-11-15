# TechRoute Recommender Human Evaluation

- **Evaluator:** Ahmed Ali, Web Developer
- **Date:** November 15, 2026
- **Model name:** gemini-3.1-flash-lite
- **Grading scale:** Pass / Partial / Fail

## Evaluation criteria

- **Relevant to target track:** Pass when the recommended resources meaningfully support the profile's selected career track.
- **Sensible beginner order:** Pass when the stages progress in a practical order for the learner's stated experience.
- **No invented or off-topic items:** Pass when opportunities are grounded in the retrieved dataset and relevant to the path.
- **Apply step realistic for skill level:** Pass when the Apply stage is suitable for the learner or honestly states that no opportunities are available.
- **Explanations clear:** Pass when the goals and reasons are understandable and useful to the learner.
- **Overall:** A holistic judgment of whether the route is useful and appropriate for this profile.
- **Notes:** Record observations that explain or qualify the ratings.

## Runs

### IT Support beginner

**Command:** `python -m src.main --profile it_support_beginner`

```text
Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Gain a broad understanding of IT support roles and essential Windows-based troubleshooting concepts.
   Opportunities: CompTIA A+ Core 2 videos, Computer Support Specialist
   Why: These resources provide the necessary background on the industry and the specific software environment required for entry-level IT support.
2. Build Skills: Develop hands-on technical proficiency by setting up virtual environments to practice system configuration.
   Opportunities: Home lab: Windows and Linux VMs in VirtualBox, Linux Essentials
   Why: Building virtual machines allows you to practice hardware and software troubleshooting safely in a controlled, self-paced environment.
3. Prove Skills: Demonstrate practical administrative capabilities and ticketing system familiarity.
   Opportunities: Home lab: help desk ticketing and Active Directory users, Google IT Support Professional Certificate
   Why: These resources confirm your ability to manage users and solve common help desk problems in a simulated professional setting.
4. Apply: Transition into professional IT support roles.
   Why: No internship or job opportunities are in the dataset yet.
```

### Networking student

**Command:** `python -m src.main --profile networking_student`

```text
Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Gain a theoretical understanding of networking concepts and the role of network administrators.
   Opportunities: Networking Basics, Network and Computer Systems Administrator
   Why: Establishing a conceptual baseline is necessary before engaging in practical simulations or labs.
2. Build Skills: Learn how to use simulation software and understand standard device configurations.
   Opportunities: CompTIA Network+ videos, Getting Started with Cisco Packet Tracer, Networking Devices and Initial Configuration
   Why: These resources provide the specific technical knowledge and tool proficiency required to build functional networks.
3. Prove Skills: Demonstrate practical networking abilities through hands-on simulation projects.
   Opportunities: Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
   Why: Applying theoretical knowledge to simulated environments validates your ability to configure and troubleshoot real-world network traffic.
4. Apply: Transition skills to real-world applications.
   Why: No internship or job opportunities are in the dataset yet.
```

### Cybersecurity beginner

**Command:** `python -m src.main --profile cybersecurity_beginner`

```text
Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Gain an entry-level understanding of core cybersecurity concepts and terminologies.
   Opportunities: Introduction to Cybersecurity, Pre Security
   Why: These resources are designed for beginners to build a conceptual base in security, Linux, and networking fundamentals without a steep learning curve.
2. Build Skills: Develop technical proficiency in security domains and practical Linux command-line interaction.
   Opportunities: Cyber Security 101, CS50 Cybersecurity, OverTheWire Bandit
   Why: This stage transitions into applied learning, allowing you to practice security concepts and Linux skills through interactive courses and project-based challenges.
3. Prove Skills: Consolidate your knowledge and prepare for industry-recognized professional standards.
   Opportunities: Junior Cybersecurity Analyst career path, CompTIA Security+ videos, Security Compliance and Identity Fundamentals SC-900
   Why: These resources align with industry certifications and professional career tracks, helping to validate your competency in security, compliance, and identity management.
4. Apply: Utilize your accumulated knowledge to seek real-world experience.
   Why: No internship or job opportunities are in the dataset yet; focus on completing your technical foundational training before pursuing placement.
```

### Cloud career changer

**Command:** `python -m src.main --profile cloud_career_changer`

```text
Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Gain a baseline understanding of cloud concepts and terminology.
   Opportunities: AZ-900 learning paths, AWS Cloud Practitioner Essentials
   Why: These resources provide the necessary conceptual framework for cloud computing at a beginner level.
2. Build Skills: Engage in structured learning and hands-on practice environments.
   Opportunities: AWS Educate, Cloud Engineering
   Why: These programs offer a structured environment to build technical skills relevant to your target track.
3. Prove Skills: Validate foundational knowledge through official credentials and practical implementation.
   Opportunities: Home lab: static site on AWS or Azure free tier, Azure Fundamentals AZ-900, AWS Certified Cloud Practitioner
   Why: These certifications and projects demonstrate your proficiency and ability to apply cloud principles to real-world tasks.
4. Apply: Transition knowledge toward professional opportunities.
   Why: No internship or job opportunities are in the dataset yet.
```

### AI Engineering student

**Command:** `python -m src.main --profile ai_engineering_student`

```text
Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Understand the scope of the AI engineering field and acquire basic language and data handling proficiency.
   Opportunities: AI Engineer, Kaggle Learn Python Pandas and Intro to Machine Learning
   Why: Establishing a foundational roadmap and core Python data skills is essential before tackling complex AI engineering concepts.
2. Build Skills: Develop core technical competencies in data analysis and machine learning through structured learning programs.
   Opportunities: Data Analysis with Python, Machine Learning with Python, AI Engineering, CS50 AI
   Why: These programs provide the necessary depth in Python-based data analysis and machine learning required for an AI engineering track.
3. Prove Skills: Apply theoretical knowledge to practical, hands-on tasks to demonstrate competency.
   Opportunities: Titanic competition, Applied AI app with local model
   Why: Project-based work confirms that you can implement models and analyze data in real-world scenarios.
4. Apply: Transition into professional practice by seeking employment or internships.
   Why: No internship or job opportunities are in the dataset yet.
```

### Software Engineering student

**Command:** `python -m src.main --profile software_engineering_student`

```text
Generated learning path - Source: Gemini (verified against retrieved data):

1. Foundations: Gain core programming proficiency and essential version control skills.
   Opportunities: CS50P, GitHub Skills courses
   Why: Establishing a strong base in Python and Git is critical for software engineering.
2. Build Skills: Develop a broader understanding of computer science and access professional development tools.
   Opportunities: CS50x, GitHub Student Developer Pack
   Why: Gaining broader technical knowledge and access to industry tools helps align with software engineering workflows.
3. Prove Skills: Demonstrate technical competence through practical application and collaborative development.
   Opportunities: CS50x final project, Open source contributions with good first issues
   Why: Building a project and contributing to existing codebases validates skills to potential employers.
4. Apply: Secure real-world experience to transition into a software engineering career.
   Opportunities: Outreachy internships, MLH Fellowship
   Why: Structured internship programs offer the necessary experience to bridge the gap between learning and professional employment.
```

### Cybersecurity beginner — offline

**Command:** `python -m src.main --profile cybersecurity_beginner --offline`

```text
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

## Evaluation table

| Profile | Source (Gemini/Fallback) | Relevant to target track | Sensible beginner order | No invented or off-topic items | Apply step realistic for skill level | Explanations clear | Overall | Notes |
|---|---|---|---|---|---|---|---|---|
| it_support_beginner | Gemini |pass  | pass | pass |  pass |  pass |  pass |  |
| networking_student | Gemini |pass   | pass |pass   | pass  | pass  | pass  |  |
| cybersecurity_beginner | Gemini | pass  | pass  | pass  |  pass | pass  | pass  |  |
| cloud_career_changer | Gemini |pass   | Pass |Pass  | Pass | Pass | Pass |  |
| ai_engineering_student | Gemini |  Pass| Pass |  v| Pass | Pass |Pass  |  |
| software_engineering_student | Gemini |Pass  | Pass | Pass |  Pass| Pass | Pass |  |
| cybersecurity_beginner --offline | Fallback |  pass |  Partial|  Pass|  Pass|Pass  | Partial |  |

## Summary

Overall result:

Main strength:

Main issue found:

## Evaluator's written summary

RAG Reliability Evaluation – Summary
The RAG Reliability Evaluation was conducted on November 14, 2026, to assess the accuracy, relevance, consistency, and reliability of the learning-resource recommendation and career-path generation system.

The evaluation used a dataset of 87 learning opportunities and tested five different learner profiles:
1. IT Support Beginner
2. Networking Student
3. Cybersecurity Beginner
4. Cloud Career Changer
5. AI Engineering Student
1. Online Evaluation (Gemini)
- Total checks: 41
- Passed: 41
- Failed: 0
- Pass rate: 100%
- Career-path generation: 6 paths generated using Gemini.
- Consistency test: 100% title overlap between repeated runs.
All five learner profiles received five relevant recommendations. The system successfully respected career-track preferences, remote-learning requirements, prerequisites, and other learner preferences.

Gemini also generated structured career paths consisting of four stages: Foundations, Build Skills, Prove Skills, and Apply. All recommendations were grounded in retrieved dataset entries, with no invented internships or job opportunities.
2. Offline Evaluation (Rule-Based Fallback)
- Total checks: 40
- Passed: 40
- Failed: 0
- Pass rate: 100%
- Career-path generation: 5 paths generated using the rule-based fallback.
When Gemini was offline, the system successfully switched to its rule-based fallback mechanism. All five learner profiles still received relevant recommendations, and the system maintained its grounding, prerequisite, remote-learning, and result-count requirements.

The fallback also maintained the four-stage career-path structure and correctly indicated when no matching internship or job opportunities were available.
3. Overall Results
Evaluation	Online	Offline
Total checks	41	40
Passed	41	40
Failed	0	0
Pass rate	100%	100%
Career paths	6	5
AI generation	Gemini	Rule-based

4. Conclusion
The evaluation demonstrates that the RAG recommendation system performed successfully in both online and offline environments. It consistently returned relevant learning opportunities, respected user preferences, generated structured career paths, and avoided introducing opportunities that were not present in the retrieved dataset.

The online evaluation also confirmed consistent Gemini-generated results across repeated runs, achieving 100% title overlap.

Final outcome: All 81 evaluation checks passed, with zero failures across both environments.

The results indicate that the system is functioning reliably under the tested conditions, with the rule-based fallback providing an alternative when Gemini is unavailable. Further testing with larger datasets, additional learner profiles, and real-world user scenarios would help validate its reliability beyond the current evaluation.
