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
Agent repair attempts used: 0
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: Computer Support Specialist, CompTIA A+ Core 2 videos, Linux Essentials
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
Source: rule-based fallback (reason: offline mode)
Agent repair attempts used: 0
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: Network and Computer Systems Administrator, Networking Basics, Networking Devices and Initial Configuration
   Why: Begin with courses and other foundational learning resources.
2. Build Skills: Practice with retrieved tools and hands-on labs.
   Opportunities: Getting Started with Cisco Packet Tracer, Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
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
Source: rule-based fallback (reason: offline mode)
Agent repair attempts used: 0
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: Introduction to Cybersecurity, Pre Security, Cyber Security 101
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
Source: rule-based fallback (reason: offline mode)
Agent repair attempts used: 0
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: AWS Cloud Practitioner Essentials, AWS Educate, AZ-900 learning paths
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
Source: rule-based fallback (reason: offline mode)
Agent repair attempts used: 0
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: AI Engineer, Kaggle Learn Python Pandas and Intro to Machine Learning, AI Engineering
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
Source: rule-based fallback (reason: offline mode)
Agent repair attempts used: 0
1. Foundations: Build foundational knowledge from retrieved learning resources.
   Opportunities: GitHub Skills courses, CS50P, CS50x
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
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== Final summary ===
Total checks: 66
Passed: 66
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
1. Foundations: Gain a baseline understanding of computer hardware, operating system navigation, and fundamental IT support concepts.
   Opportunities: CompTIA A+ Core 2 videos
   Why: Establishing a strong knowledge base in Windows environments and hardware components is essential for effectively supporting users and diagnosing technical issues.
2. Build Skills: Develop hands-on experience by creating virtual environments to practice troubleshooting hardware and software configurations safely.
   Opportunities: Home lab: Windows and Linux VMs in VirtualBox, Linux Essentials
   Why: Building a home lab allows for repeatable, risk-free practice in managing virtual operating systems, which is critical for developing methodical troubleshooting techniques.
3. Prove Skills: Demonstrate the ability to handle administrative tasks and manage technical requests within a simulated professional environment.
   Opportunities: Home lab: help desk ticketing and Active Directory users
   Why: This project bridges the gap between theoretical knowledge and practical application by simulating real-world ticket workflows and user management.
4. Apply: Understand the scope, responsibilities, and career trajectory of professional IT support roles to align future efforts.
   Opportunities: none
   Why: Reviewing official career documentation helps you understand industry expectations for remote IT support. Please note that no internship or job opportunities are in the dataset yet.
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
1. Foundations: Gain a solid understanding of how networking devices communicate and the role of IP addressing in data transmission.
   Opportunities: Networking Basics
   Why: This course provides the essential theoretical framework for understanding network connectivity, protocols, and how devices interact within a network.
2. Build Skills: Develop practical configuration skills using virtualized networking environments to manage IP addressing and hardware.
   Opportunities: Getting Started with Cisco Packet Tracer, Networking Devices and Initial Configuration
   Why: These resources provide hands-on practice for managing virtual network environments and configuring devices, which is critical for mastering network administration.
3. Prove Skills: Apply theoretical knowledge and configuration skills to troubleshoot and verify connectivity within a controlled network simulation.
   Opportunities: Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
   Why: Completing project-based labs allows for the practical application of troubleshooting techniques and packet analysis, which are core competencies for network technicians.
4. Apply: Align technical skills with professional career requirements to prepare for future entry-level networking roles.
   Opportunities: none
   Why: Reviewing professional career information helps bridge the gap between lab-based learning and real-world responsibilities; no internship or job opportunities are in the dataset yet.
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
1. Foundations: Gain a baseline understanding of security concepts, networking, and operating systems.
   Opportunities: Introduction to Cybersecurity, Pre Security
   Why: These resources establish the necessary groundwork in networking, security terminology, and operating system basics required for your cybersecurity track.
2. Build Skills: Develop practical experience with Linux commands and deepen security knowledge through study.
   Opportunities: OverTheWire Bandit, CompTIA Security+ videos
   Why: This combination of hands-on Linux practice and formal theoretical review helps you apply security concepts in a practical environment.
3. Prove Skills: Demonstrate understanding by reviewing security fundamentals and exploring professional career paths.
   Opportunities: CS50 Cybersecurity, Junior Cybersecurity Analyst career path
   Why: These advanced learning opportunities allow you to synthesize your technical knowledge and align your skills with industry-standard career expectations.
4. Apply: Prepare to translate your foundational skills and project experience into entry-level cybersecurity roles.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet, so use this stage to organize your notes, lab documentation, and learning evidence for future applications.
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
1. Foundations: Gain an understanding of core cloud infrastructure concepts, including virtual machines, storage, networking, and identity management in a cloud environment.
   Opportunities: AZ-900 learning paths, AWS Cloud Practitioner Essentials
   Why: These foundational resources provide the necessary terminology and conceptual understanding of cloud service models and shared responsibility required to navigate cloud platforms.
2. Build Skills: Develop practical experience by deploying a small, isolated cloud environment and configuring its network and access settings.
   Opportunities: Home lab: static site on AWS or Azure free tier
   Why: Building an isolated environment allows for the application of theory to practice, helping to reinforce concepts like compute and storage configuration within a restricted time frame.
3. Prove Skills: Demonstrate technical competence and foundational knowledge through official certification.
   Opportunities: Azure Fundamentals AZ-900, AWS Certified Cloud Practitioner
   Why: Earning a certification validates the skills and knowledge acquired during the foundational and skill-building phases, proving a standard level of cloud literacy.
4. Apply: Transition knowledge toward professional roles by participating in structured learning programs that emphasize practical application.
   Opportunities: none
   Why: This step encourages the structured application of existing cloud knowledge; please note that no internship or job opportunities are in the dataset yet.
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
1. Foundations: Establish a core understanding of Python programming, data manipulation, and the fundamental concepts of machine learning.
   Opportunities: AI Engineer, Kaggle Learn Python Pandas and Intro to Machine Learning
   Why: These resources provide the structural roadmap and entry-level technical training necessary to begin your journey in AI engineering.
2. Build Skills: Gain practical experience in data preparation and model application by working through a structured predictive challenge.
   Opportunities: Titanic competition
   Why: This project allows you to apply Python and data analysis skills to a real-world dataset, helping you understand the basics of model training and evaluation.
3. Prove Skills: Develop an end-to-end AI application to demonstrate your ability to integrate models into functional software.
   Opportunities: Applied AI app with local model
   Why: Building a hands-on project is the most effective way to demonstrate your competency in connecting model logic with application development.
4. Apply: Synthesize your project findings and prepare to communicate your technical process and model limitations.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet; focus on documenting your project architecture, evaluation results, and failure cases.
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
1. Foundations: Gain a solid grasp of programming fundamentals, specifically focusing on syntax, control flow, and data structures using Python.
   Opportunities: CS50P
   Why: This self-paced course provides a structured introduction to programming fundamentals in Python, which is essential for building a strong base in software engineering.
2. Build Skills: Learn to manage code, track changes, and collaborate using version control systems.
   Opportunities: GitHub Skills courses, GitHub Student Developer Pack
   Why: Mastering version control is a core requirement for software engineering; these resources offer practical exercises to manage code effectively.
3. Prove Skills: Develop and document a functional project to demonstrate technical proficiency and problem-solving abilities.
   Opportunities: CS50x final project, Open source contributions with good first issues
   Why: Completing a project and contributing to existing codebases allows you to demonstrate your ability to solve defined problems and collaborate with others.
4. Apply: Gain real-world experience in a professional, remote-first software engineering environment.
   Opportunities: Outreachy internships, MLH Fellowship
   Why: These internships provide the hands-on, collaborative experience necessary to transition from a student learner to a professional software engineer.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: 2 internship/job item(s) retrieved
PASS: Apply step contains at least one retrieved internship/job: Apply includes retrieved opportunity: MLH Fellowship, Outreachy internships
PASS: Source label: Source: Gemini (verified against retrieved data)
PASS: Agent: stage size <= 3: all stages contain at most 3 opportunities
PASS: Agent: no duplicate titles: no opportunity title appears across multiple stages

=== Cloud career changer consistency run ===
FAIL: Gemini consistency: overlap unavailable because one or both Gemini runs fell back to the rule-based path
Second run source: Source: rule-based fallback (reason: AI output failed verification after 2 repair attempts)
Consistency run repair attempts used: 2
Consistency overlap: FAIL: overlap unavailable because one or both Gemini runs fell back to the rule-based path

=== Final summary ===
Total checks: 67
Passed: 66
Failed: 1
Pass rate: 98.5%
Paths from Gemini: 6
Paths from fallback: 1
Consistency overlap: FAIL: overlap unavailable because one or both Gemini runs fell back to the rule-based path
```
