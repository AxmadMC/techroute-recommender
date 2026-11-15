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
Source: rule-based fallback (reason: Gemini API error)
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
PASS: Source label: Source: rule-based fallback (reason: Gemini API error)

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
1. Foundations: Gain a baseline understanding of networking concepts and the industry landscape.
   Opportunities: Networking Basics, Network and Computer Systems Administrator
   Why: Establishing a theoretical understanding of networking fundamentals and career paths is essential before hands-on practice.
2. Build Skills: Acquire technical knowledge on networking devices and simulation software.
   Opportunities: CompTIA Network+ videos, Getting Started with Cisco Packet Tracer, Networking Devices and Initial Configuration
   Why: These resources provide the specific expertise needed to manipulate network hardware configurations and navigate simulation environments effectively.
3. Prove Skills: Demonstrate proficiency through practical, project-based network modeling.
   Opportunities: Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
   Why: Applying theoretical knowledge to simulated environments and packet analysis confirms your ability to troubleshoot and design small-scale networks.
4. Apply: Transition skills into a professional context.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)

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
1. Foundations: Gain an entry-level understanding of core cybersecurity concepts and terminology.
   Opportunities: Introduction to Cybersecurity, Cyber Security 101, Pre Security
   Why: These resources establish the basic vocabulary and fundamental principles required for the cybersecurity track.
2. Build Skills: Develop technical proficiency in networking and system security through structured courses.
   Opportunities: CS50 Cybersecurity, CompTIA Security+ videos, Junior Cybersecurity Analyst career path
   Why: This stage builds deep knowledge across the target interest areas of networking and security fundamentals.
3. Prove Skills: Validate knowledge through hands-on practice and industry-recognized learning paths.
   Opportunities: Security Compliance and Identity Fundamentals SC-900, OverTheWire Bandit
   Why: Testing skills in a practical environment and preparing for fundamental certification demonstrates capability to potential stakeholders.
4. Apply: Transition skills into professional practice.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)

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
1. Foundations: Gain a broad understanding of cloud computing principles and terminology.
   Opportunities: AZ-900 learning paths, AWS Cloud Practitioner Essentials
   Why: Establishing a conceptual baseline is necessary before engaging with specific cloud provider tools and services.
2. Build Skills: Gain practical experience with cloud environments and infrastructure basics.
   Opportunities: AWS Educate, Cloud Engineering
   Why: Engaging in structured programs allows for interactive skill development within the cloud domain.
3. Prove Skills: Demonstrate technical competency through official industry certifications.
   Opportunities: Azure Fundamentals AZ-900, AWS Certified Cloud Practitioner
   Why: Certifications validate your foundational knowledge and are recognized benchmarks for entry-level cloud proficiency.
4. Apply: Implement knowledge through hands-on technical projects and prepare for professional opportunities.
   Opportunities: none
   Why: Building a project like Home lab: static site on AWS or Azure free tier provides tangible proof of skills, though no internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)

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
1. Foundations: Understand the scope of the AI engineering field and gain basic Python and machine learning literacy.
   Opportunities: AI Engineer, Kaggle Learn Python Pandas and Intro to Machine Learning
   Why: Establishing a foundational roadmap and initial technical knowledge is essential before starting complex projects.
2. Build Skills: Develop deep technical proficiency in data analysis and machine learning algorithms using Python.
   Opportunities: Data Analysis with Python, Machine Learning with Python, AI Engineering, CS50 AI
   Why: These structured programs provide the necessary theoretical and practical depth required for AI engineering.
3. Prove Skills: Demonstrate the ability to apply data science and AI concepts to solve practical problems.
   Opportunities: Titanic competition, Applied AI app with local model
   Why: Applying learned concepts through projects and competitions validates skills and builds a project portfolio.
4. Apply: Transition knowledge into professional experience.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Apply step contains at least one retrieved internship/job: not applicable: no internship/job rows were retrieved
PASS: Source label: Source: Gemini (verified against retrieved data)

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
1. Foundations: Gain core programming proficiency in Python and understand computer science fundamentals.
   Opportunities: CS50P, CS50x
   Why: These courses provide a structured introduction to programming logic and the Python language, which are essential for a software engineering career.
2. Build Skills: Master version control systems and professional development tools.
   Opportunities: GitHub Skills courses, GitHub Student Developer Pack
   Why: Learning how to use Git and professional development tools is necessary for collaborative software engineering and managing codebases.
3. Prove Skills: Demonstrate technical capability through independent project work and collaborative development.
   Opportunities: CS50x final project, Open source contributions with good first issues
   Why: Building a custom project and contributing to existing codebases validates your skills to potential employers and builds practical experience.
4. Apply: Transition into professional roles through structured internship programs.
   Opportunities: Outreachy internships, MLH Fellowship
   Why: Participating in recognized internship programs provides the real-world experience and professional network needed to secure a full-time position.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: 2 internship/job item(s) retrieved
PASS: Apply step contains at least one retrieved internship/job: Apply includes retrieved opportunity: MLH Fellowship, Outreachy internships
PASS: Source label: Source: Gemini (verified against retrieved data)

=== Cloud career changer consistency run ===
PASS: Gemini consistency: title overlap 85.7% (Jaccard; threshold 70%)
Second run source: Source: Gemini (verified against retrieved data)
Consistency overlap: PASS: title overlap 85.7% (Jaccard; threshold 70%)

=== Final summary ===
Total checks: 55
Passed: 55
Failed: 0
Pass rate: 100.0%
Paths from Gemini: 6
Paths from fallback: 1
Consistency overlap: PASS: title overlap 85.7% (Jaccard; threshold 70%)
```
