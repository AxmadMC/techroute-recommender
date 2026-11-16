# RAG Reliability Evaluation

- Command: `python scripts/evaluate_reliability.py --offline`
- Date: 2026-11-15

```text
Command: python scripts/evaluate_reliability.py --offline
Date: 2026-11-15
Dataset rows: 87
Gemini mode: offline

=== IT Support beginner ===
Input profile: {'target_track': 'it_support', 'preferred_format': 'self_paced', 'skill_level': 0.2, 'prefers_free': True, 'needs_remote': True, 'max_hours': 10, 'interests': ['hardware', 'troubleshooting', 'windows']}
1. CompTIA A+ Core 2 videos | Professor Messer | score=5.83
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
2. Linux Essentials | Cisco NetAcad | score=5.50
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
3. Home lab: Windows and Linux VMs in VirtualBox | Self-directed | score=5.17
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
4. Google IT Support Professional Certificate | Google | score=5.17
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
5. Home lab: help desk ticketing and Active Directory users | Self-directed | score=4.98
   career track match (+2.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.42); interest overlap (+0.17)
PASS: Track relevance: 5/5 recommendations match it_support
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: CompTIA A+ Core 2 videos has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: rule-based fallback (reason: offline mode)
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: Computer Support Specialist, CompTIA A+ Core 2 videos, Linux Essentials, Per Scholas IT Support
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Opportunities: Home lab: Windows and Linux VMs in VirtualBox, Home lab: help desk ticketing and Active Directory users
   Why: These retrieved resources provide practical tool or lab experience.
3. Prove Skills: Demonstrate skills with retrieved projects and credentials.
   Opportunities: Google IT Support Professional Certificate, CompTIA A+
   Why: Projects, certifications, and contributions can demonstrate progress.
4. Apply: No internship or job opportunities are in the dataset yet for this track.
   Opportunities: none
   Why: No matching internship or job rows were retrieved.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: rule-based fallback (reason: offline mode)

=== Networking student ===
Input profile: {'target_track': 'networking', 'preferred_format': 'project_based', 'skill_level': 0.35, 'prefers_free': True, 'needs_remote': True, 'max_hours': 8, 'interests': ['networking', 'ip_addressing', 'packet_tracer']}
1. Home lab: packet capture with Wireshark | Self-directed | score=6.12
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
2. Home lab: small-office network in Packet Tracer | Self-directed | score=6.02
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.85); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
3. CompTIA Network+ videos | Professor Messer | score=4.78
   career track match (+2.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
4. Getting Started with Cisco Packet Tracer | Cisco Skills for All | score=4.68
   career track match (+2.00); difficulty fit (+0.85); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
5. Networking Basics | Cisco Skills for All | score=4.58
   career track match (+2.00); difficulty fit (+0.75); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
PASS: Track relevance: 5/5 recommendations match networking
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: Home lab: packet capture with Wireshark has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: rule-based fallback (reason: offline mode)
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: Network and Computer Systems Administrator, Networking Basics, Networking Devices and Initial Configuration, CompTIA Network+ videos
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Opportunities: Getting Started with Cisco Packet Tracer, Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark, Home lab: static site on AWS or Azure free tier
   Why: These retrieved resources provide practical tool or lab experience.
3. Prove Skills: Demonstrate skills with retrieved projects and credentials.
   Opportunities: none
   Why: Projects, certifications, and contributions can demonstrate progress.
4. Apply: No internship or job opportunities are in the dataset yet for this track.
   Opportunities: none
   Why: No matching internship or job rows were retrieved.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: rule-based fallback (reason: offline mode)

=== Cybersecurity beginner ===
Input profile: {'target_track': 'cybersecurity', 'preferred_format': 'self_paced', 'skill_level': 0.2, 'prefers_free': True, 'needs_remote': True, 'max_hours': 5, 'interests': ['security_fundamentals', 'linux', 'networking']}
1. CS50 Cybersecurity | Harvard CS50 | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
2. Introduction to Cybersecurity | Cisco Skills for All | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
3. Junior Cybersecurity Analyst career path | Cisco Skills for All | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
4. CompTIA Security+ videos | Professor Messer | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
5. Cyber Security 101 | TryHackMe | score=5.50
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.50)
PASS: Track relevance: 5/5 recommendations match cybersecurity
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: CS50 Cybersecurity has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: rule-based fallback (reason: offline mode)
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: Introduction to Cybersecurity, Pre Security, Cyber Security 101, CS50 Cybersecurity, CompTIA Security+ videos, Junior Cybersecurity Analyst career path
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Opportunities: none
   Why: These retrieved resources provide practical tool or lab experience.
3. Prove Skills: Demonstrate skills with retrieved projects and credentials.
   Opportunities: OverTheWire Bandit, Security Compliance and Identity Fundamentals SC-900
   Why: Projects, certifications, and contributions can demonstrate progress.
4. Apply: No internship or job opportunities are in the dataset yet for this track.
   Opportunities: none
   Why: No matching internship or job rows were retrieved.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: rule-based fallback (reason: offline mode)

=== Cloud career changer ===
Input profile: {'target_track': 'cloud_computing', 'preferred_format': 'self_paced', 'skill_level': 0.3, 'prefers_free': True, 'needs_remote': True, 'max_hours': 10, 'interests': ['azure', 'cloud', 'linux']}
1. AZ-900 learning paths | Microsoft Learn | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
2. AWS Cloud Practitioner Essentials | AWS Skill Builder | score=5.40
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
3. AWS Educate | AWS Educate | score=5.40
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
4. Home lab: static site on AWS or Azure free tier | Self-directed | score=5.17
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
5. Azure Fundamentals AZ-900 | Microsoft Learn | score=5.07
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
PASS: Track relevance: 5/5 recommendations match cloud_computing
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: AZ-900 learning paths has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: rule-based fallback (reason: offline mode)
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: AWS Cloud Practitioner Essentials, AWS Educate, AZ-900 learning paths, Google Cloud Skills Boost no cost labs, Cloud Engineering
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Opportunities: Home lab: static site on AWS or Azure free tier
   Why: These retrieved resources provide practical tool or lab experience.
3. Prove Skills: Demonstrate skills with retrieved projects and credentials.
   Opportunities: AWS Certified Cloud Practitioner, Azure Fundamentals AZ-900
   Why: Projects, certifications, and contributions can demonstrate progress.
4. Apply: No internship or job opportunities are in the dataset yet for this track.
   Opportunities: none
   Why: No matching internship or job rows were retrieved.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: rule-based fallback (reason: offline mode)

=== AI Engineering student ===
Input profile: {'target_track': 'ai_engineering', 'preferred_format': 'project_based', 'skill_level': 0.35, 'prefers_free': True, 'needs_remote': True, 'max_hours': 12, 'interests': ['python', 'machine_learning', 'data_analysis']}
1. Titanic competition | Kaggle | score=6.45
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.50)
2. Applied AI app with local model | Self-directed | score=5.92
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.30); interest overlap (+0.17)
3. Data Analysis with Python | freeCodeCamp | score=5.80
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.02); interest overlap (+0.33)
4. Machine Learning with Python | freeCodeCamp | score=5.80
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.02); interest overlap (+0.33)
5. CS50 AI | Harvard CS50 | score=4.78
   career track match (+2.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
PASS: Track relevance: 5/5 recommendations match ai_engineering
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: Titanic competition has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: rule-based fallback (reason: offline mode)
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: AI Engineer, Kaggle Learn Python Pandas and Intro to Machine Learning, AI Engineering, CS50 AI
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Opportunities: Applied AI app with local model
   Why: These retrieved resources provide practical tool or lab experience.
3. Prove Skills: Demonstrate skills with retrieved projects and credentials.
   Opportunities: Data Analysis with Python, Titanic competition, Machine Learning with Python
   Why: Projects, certifications, and contributions can demonstrate progress.
4. Apply: No internship or job opportunities are in the dataset yet for this track.
   Opportunities: none
   Why: No matching internship or job rows were retrieved.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: rule-based fallback (reason: offline mode)

=== Software Engineering student ===
Input profile: {'target_track': 'software_engineering', 'preferred_format': 'self_paced', 'skill_level': 0.3, 'prefers_free': True, 'needs_remote': True, 'max_hours': 20, 'interests': ['python', 'git']}
1. CS50P | Harvard CS50 | score=5.65
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.25)
2. CS50x | Harvard CS50 | score=5.40
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
3. CS50x final project | Harvard CS50 | score=5.00
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50)
4. Open source contributions with good first issues | GitHub | score=4.75
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.25)
5. Outreachy internships | Outreachy | score=4.65
   career track match (+2.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.25)
PASS: Track relevance: 5/5 recommendations match software_engineering
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: CS50P has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: rule-based fallback (reason: offline mode)
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: GitHub Skills courses, CS50P, CS50x, GitHub Student Developer Pack
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Opportunities: none
   Why: These retrieved resources provide practical tool or lab experience.
3. Prove Skills: Demonstrate skills with retrieved projects and credentials.
   Opportunities: CS50x final project, Open source contributions with good first issues
   Why: Projects, certifications, and contributions can demonstrate progress.
4. Apply: Use the retrieved internship or job opportunities to apply.
   Opportunities: MLH Fellowship, Outreachy internships
   Why: These are the available next-step opportunities in the retrieved data.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: 2 internship/job item(s) retrieved
PASS: Apply step contains at least one retrieved internship/job: Apply includes retrieved opportunity: MLH Fellowship, Outreachy internships
PASS: Source label: Source: rule-based fallback (reason: offline mode)

=== Final summary ===
Total checks: 54
Passed: 54
Failed: 0
Pass rate: 100.0%
Paths from Gemini: 0
Paths from fallback: 6
Consistency overlap: Not run (offline mode)
```


---

# RAG Reliability Evaluation

- Command: `python scripts/evaluate_reliability.py`
- Date: 2026-11-15

```text
Command: python scripts/evaluate_reliability.py
Date: 2026-11-15
Dataset rows: 87
Gemini mode: online

=== IT Support beginner ===
Input profile: {'target_track': 'it_support', 'preferred_format': 'self_paced', 'skill_level': 0.2, 'prefers_free': True, 'needs_remote': True, 'max_hours': 10, 'interests': ['hardware', 'troubleshooting', 'windows']}
1. CompTIA A+ Core 2 videos | Professor Messer | score=5.83
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
2. Linux Essentials | Cisco NetAcad | score=5.50
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
3. Home lab: Windows and Linux VMs in VirtualBox | Self-directed | score=5.17
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
4. Google IT Support Professional Certificate | Google | score=5.17
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
5. Home lab: help desk ticketing and Active Directory users | Self-directed | score=4.98
   career track match (+2.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.42); interest overlap (+0.17)
PASS: Track relevance: 5/5 recommendations match it_support
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: CompTIA A+ Core 2 videos has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: Gemini (verified against retrieved data)
Agent repair attempts used: 0
1. Foundations: Gain a clear understanding of the IT support career track and industry expectations.
   Opportunities: Computer Support Specialist
   Why: This provides a baseline knowledge of the role and what is expected of professionals in the field.
2. Build Skills: Develop technical knowledge in hardware and Windows troubleshooting.
   Opportunities: CompTIA A+ Core 2 videos, Linux Essentials
   Why: These free, self-paced resources align with your interests in hardware and operating systems.
3. Prove Skills: Apply theoretical knowledge through practical, hands-on troubleshooting exercises.
   Opportunities: Home lab: Windows and Linux VMs in VirtualBox, Home lab: help desk ticketing and Active Directory users
   Why: These projects allow you to practice real-world tasks in a controlled, virtual environment.
4. Apply: Prepare for the transition into professional IT support roles.
   Opportunities: none
   Why: This stage focuses on career readiness; note that no specific internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== Networking student ===
Input profile: {'target_track': 'networking', 'preferred_format': 'project_based', 'skill_level': 0.35, 'prefers_free': True, 'needs_remote': True, 'max_hours': 8, 'interests': ['networking', 'ip_addressing', 'packet_tracer']}
1. Home lab: packet capture with Wireshark | Self-directed | score=6.12
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
2. Home lab: small-office network in Packet Tracer | Self-directed | score=6.02
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.85); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
3. CompTIA Network+ videos | Professor Messer | score=4.78
   career track match (+2.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
4. Getting Started with Cisco Packet Tracer | Cisco Skills for All | score=4.68
   career track match (+2.00); difficulty fit (+0.85); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
5. Networking Basics | Cisco Skills for All | score=4.58
   career track match (+2.00); difficulty fit (+0.75); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
PASS: Track relevance: 5/5 recommendations match networking
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: Home lab: packet capture with Wireshark has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: Gemini (verified against retrieved data)
Agent repair attempts used: 0
1. Foundations: Gain a solid understanding of fundamental networking concepts.
   Opportunities: Networking Basics, CompTIA Network+ videos
   Why: These resources establish the necessary conceptual framework for networking required for a beginner.
2. Build Skills: Develop practical proficiency in networking tools and device configuration.
   Opportunities: Getting Started with Cisco Packet Tracer, Networking Devices and Initial Configuration
   Why: These courses align with your interest in Packet Tracer and help you learn to configure networking equipment.
3. Prove Skills: Apply theoretical knowledge to solve real-world networking scenarios.
   Opportunities: Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
   Why: These project-based assignments validate your understanding of IP addressing and network traffic analysis.
4. Apply: Transition your skills into professional opportunities.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== Cybersecurity beginner ===
Input profile: {'target_track': 'cybersecurity', 'preferred_format': 'self_paced', 'skill_level': 0.2, 'prefers_free': True, 'needs_remote': True, 'max_hours': 5, 'interests': ['security_fundamentals', 'linux', 'networking']}
1. CS50 Cybersecurity | Harvard CS50 | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
2. Introduction to Cybersecurity | Cisco Skills for All | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
3. Junior Cybersecurity Analyst career path | Cisco Skills for All | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
4. CompTIA Security+ videos | Professor Messer | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
5. Cyber Security 101 | TryHackMe | score=5.50
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+1.00); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.50)
PASS: Track relevance: 5/5 recommendations match cybersecurity
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: CS50 Cybersecurity has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: Gemini (verified against retrieved data)
Agent repair attempts used: 0
1. Foundations: Gain a baseline understanding of cybersecurity concepts.
   Opportunities: Introduction to Cybersecurity, CS50 Cybersecurity
   Why: These introductory resources align with your current skill level by providing a foundational overview of the cybersecurity landscape.
2. Build Skills: Develop technical proficiency in networking and Linux fundamentals.
   Opportunities: Pre Security, Cyber Security 101
   Why: The hands-on nature of these courses helps build the core networking and Linux skills necessary for your target track.
3. Prove Skills: Validate your knowledge through practical, gamified application.
   Opportunities: OverTheWire Bandit
   Why: This project allows you to apply your Linux knowledge in a practical, security-focused environment to demonstrate your proficiency.
4. Apply: Prepare for real-world application of your skills.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet; this stage focuses on synthesizing your learning to prepare for future professional roles.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== Cloud career changer ===
Input profile: {'target_track': 'cloud_computing', 'preferred_format': 'self_paced', 'skill_level': 0.3, 'prefers_free': True, 'needs_remote': True, 'max_hours': 10, 'interests': ['azure', 'cloud', 'linux']}
1. AZ-900 learning paths | Microsoft Learn | score=5.57
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
2. AWS Cloud Practitioner Essentials | AWS Skill Builder | score=5.40
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
3. AWS Educate | AWS Educate | score=5.40
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
4. Home lab: static site on AWS or Azure free tier | Self-directed | score=5.17
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.17)
5. Azure Fundamentals AZ-900 | Microsoft Learn | score=5.07
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+0.50); Remote requirement met; remote preference match (+0.50); interest overlap (+0.17)
PASS: Track relevance: 5/5 recommendations match cloud_computing
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: AZ-900 learning paths has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: Gemini (verified against retrieved data)
Agent repair attempts used: 0
1. Foundations: Gain an introductory understanding of core cloud concepts.
   Opportunities: AZ-900 learning paths
   Why: This self-paced course provides a free, introductory understanding of core Azure cloud concepts.
2. Build Skills: Develop essential hands-on cloud computing skills through structured learning programs.
   Opportunities: AWS Educate, AWS Cloud Practitioner Essentials
   Why: These programs offer hands-on, remote-friendly learning resources to build essential cloud computing skills.
3. Prove Skills: Demonstrate knowledge by creating a practical project in a real-world cloud environment.
   Opportunities: Home lab: static site on AWS or Azure free tier
   Why: Building a project allows you to apply your knowledge in a practical environment using free-tier cloud resources.
4. Apply: Transition your skills toward professional cloud engineering roles.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== AI Engineering student ===
Input profile: {'target_track': 'ai_engineering', 'preferred_format': 'project_based', 'skill_level': 0.35, 'prefers_free': True, 'needs_remote': True, 'max_hours': 12, 'interests': ['python', 'machine_learning', 'data_analysis']}
1. Titanic competition | Kaggle | score=6.45
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50); interest overlap (+0.50)
2. Applied AI app with local model | Self-directed | score=5.92
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.30); interest overlap (+0.17)
3. Data Analysis with Python | freeCodeCamp | score=5.80
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.02); interest overlap (+0.33)
4. Machine Learning with Python | freeCodeCamp | score=5.80
   career track match (+2.00); format matches 'project_based' (+1.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.02); interest overlap (+0.33)
5. CS50 AI | Harvard CS50 | score=4.78
   career track match (+2.00); difficulty fit (+0.95); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.33)
PASS: Track relevance: 5/5 recommendations match ai_engineering
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: Titanic competition has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: Gemini (verified against retrieved data)
Agent repair attempts used: 0
1. Foundations: Gain a high-level conceptual understanding of the AI engineering field and its core requirements.
   Opportunities: AI Engineer
   Why: This roadmap provides a structured overview of the AI engineering field to guide your learning path.
2. Build Skills: Develop core programming proficiency in Python and basic data handling for machine learning tasks.
   Opportunities: Kaggle Learn Python Pandas and Intro to Machine Learning
   Why: This interactive course matches your preference for quick, project-based learning in Python and data analysis.
3. Prove Skills: Demonstrate your ability to perform data analysis and build predictive models within a structured competition environment.
   Opportunities: Titanic competition
   Why: This project offers a hands-on opportunity to apply your initial machine learning knowledge in a competitive format.
4. Apply: Integrate your skills by building a functional application.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet, but building a functional application with a local model allows you to apply your skills in a practical, remote-friendly project.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== Software Engineering student ===
Input profile: {'target_track': 'software_engineering', 'preferred_format': 'self_paced', 'skill_level': 0.3, 'prefers_free': True, 'needs_remote': True, 'max_hours': 20, 'interests': ['python', 'git']}
1. CS50P | Harvard CS50 | score=5.65
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.25)
2. CS50x | Harvard CS50 | score=5.40
   career track match (+2.00); format matches 'self_paced' (+1.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50)
3. CS50x final project | Harvard CS50 | score=5.00
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); time fit (+0.50)
4. Open source contributions with good first issues | GitHub | score=4.75
   career track match (+2.00); difficulty fit (+1.00); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.25)
5. Outreachy internships | Outreachy | score=4.65
   career track match (+2.00); difficulty fit (+0.90); free priority (+1.00); Remote requirement met; remote preference match (+0.50); interest overlap (+0.25)
PASS: Track relevance: 5/5 recommendations match software_engineering
PASS: Remote guardrail: all results are remote
PASS: Prerequisite guardrail: rank #1: CS50P has no prior_experience tag
PASS: Result count: returned 5 recommendations
Retrieved opportunities for path generation: 8
Source: Gemini (verified against retrieved data)
Agent repair attempts used: 0
1. Foundations: Establish a core understanding of Python programming and essential version control practices.
   Opportunities: CS50P, GitHub Skills courses
   Why: These resources provide the necessary self-paced introduction to programming and Git required for your software engineering path.
2. Build Skills: Expand technical breadth and gain practical experience through project-based learning.
   Opportunities: CS50x, CS50x final project, GitHub Student Developer Pack
   Why: These opportunities offer a broader engineering context and tools to support independent project development.
3. Prove Skills: Demonstrate technical proficiency in a collaborative, real-world development environment.
   Opportunities: Open source contributions with good first issues
   Why: Contributing to open source projects validates your Git and coding abilities through tangible, peer-reviewed work.
4. Apply: Transition into a professional setting to gain hands-on experience under mentorship.
   Opportunities: Outreachy internships, MLH Fellowship
   Why: These remote professional programs provide the structured environment necessary to apply your skills in a career-oriented role.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: 2 internship/job item(s) retrieved
PASS: Apply step contains at least one retrieved internship/job: Apply includes retrieved opportunity: MLH Fellowship, Outreachy internships
PASS: Source label: Source: Gemini (verified against retrieved data)
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== Cloud career changer consistency run ===
FAIL: Gemini consistency: title overlap 66.7% (Jaccard; threshold 70%)
Second run source: Source: Gemini (verified against retrieved data)
Consistency run repair attempts used: 0
Consistency overlap: FAIL: title overlap 66.7% (Jaccard; threshold 70%)

=== Final summary ===
Total checks: 67
Passed: 66
Failed: 1
Pass rate: 98.5%
Paths from Gemini: 7
Paths from fallback: 0
Consistency overlap: FAIL: title overlap 66.7% (Jaccard; threshold 70%)
```
