# RAG Reliability Evaluation

- Command: `python scripts/evaluate_reliability.py`
- Date: 2026-11-14

```text
Command: python scripts/evaluate_reliability.py
Date: 2026-11-14
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
1. Foundations: Understand the scope of the IT support profession and core troubleshooting concepts for Windows environments.
   Opportunities: Computer Support Specialist, CompTIA A+ Core 2 videos
   Why: These resources provide a baseline understanding of what IT support involves and cover essential Windows troubleshooting and security protocols.
2. Build Skills: Develop technical competency in operating systems and foundational infrastructure management.
   Opportunities: Google IT Support Professional Certificate, Linux Essentials, Per Scholas IT Support
   Why: These programs build structured knowledge across hardware, software, and administrative tasks required for entry-level IT roles.
3. Prove Skills: Gain practical, hands-on experience in managing virtualized environments and help desk workflows.
   Opportunities: Home lab: Windows and Linux VMs in VirtualBox, Home lab: help desk ticketing and Active Directory users
   Why: These projects allow you to demonstrate your ability to configure systems and manage user identities in a real-world simulation.
4. Apply: Transition knowledge into professional opportunities.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Source label: Source: Gemini (verified against retrieved data)

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
1. Foundations: Gain a fundamental understanding of networking concepts and the role of network administrators.
   Opportunities: Networking Basics, Network and Computer Systems Administrator
   Why: Establishing a conceptual baseline is essential before moving into hands-on configuration or troubleshooting.
2. Build Skills: Develop technical knowledge in networking protocols and hardware configuration.
   Opportunities: CompTIA Network+ videos, Getting Started with Cisco Packet Tracer, Networking Devices and Initial Configuration
   Why: These resources provide the theoretical and software-specific knowledge required to work with networking tools effectively.
3. Prove Skills: Demonstrate practical competency by simulating network environments and analyzing data traffic.
   Opportunities: Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
   Why: Project-based learning allows for the direct application of networking principles in a controlled environment.
4. Apply: Transition skills to real-world opportunities.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
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
   Opportunities: Introduction to Cybersecurity, Pre Security
   Why: These resources provide a gentle, self-paced introduction to the field, helping to bridge the gap between basic computer literacy and security fundamentals.
2. Build Skills: Develop technical proficiency in Linux, networking, and foundational security protocols.
   Opportunities: Cyber Security 101, CS50 Cybersecurity, OverTheWire Bandit
   Why: These resources offer a hands-on approach to learning Linux command line skills and security principles, which are essential for the target cybersecurity track.
3. Prove Skills: Synthesize knowledge and demonstrate readiness for entry-level professional certification.
   Opportunities: Junior Cybersecurity Analyst career path, CompTIA Security+ videos, Security Compliance and Identity Fundamentals SC-900
   Why: These materials align with industry standards and help organize your knowledge for professional recognition.
4. Apply: Transition from learning to seeking professional opportunities in the field.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
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
1. Foundations: Gain a baseline understanding of cloud computing concepts and terminology.
   Opportunities: AZ-900 learning paths, AWS Cloud Practitioner Essentials
   Why: These resources provide the necessary conceptual framework for understanding cloud infrastructure, which is essential for a beginner.
2. Build Skills: Develop practical experience with cloud environments and educational support systems.
   Opportunities: AWS Educate, Cloud Engineering
   Why: These programs offer structured learning environments that bridge the gap between theory and practical application.
3. Prove Skills: Demonstrate proficiency through hands-on practice and formal validation.
   Opportunities: Home lab: static site on AWS or Azure free tier, Azure Fundamentals AZ-900, AWS Certified Cloud Practitioner
   Why: Completing projects and earning certifications proves your ability to navigate cloud platforms effectively.
4. Apply: Transition knowledge into professional experience.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
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
1. Foundations: Understand the scope of the AI engineering career path and learn the necessary syntax for data manipulation and basic machine learning concepts.
   Opportunities: AI Engineer, Kaggle Learn Python Pandas and Intro to Machine Learning
   Why: Establishing a strong foundation in roadmap navigation and core Python data libraries is essential before diving into complex AI projects.
2. Build Skills: Develop technical proficiency in data analysis and machine learning implementation using standard Python libraries.
   Opportunities: Data Analysis with Python, Machine Learning with Python, AI Engineering
   Why: These programs provide comprehensive structured learning that aligns with the target track of becoming an AI engineer.
3. Prove Skills: Demonstrate practical ability by solving real-world data problems and building functional applications.
   Opportunities: Titanic competition, Applied AI app with local model, CS50 AI
   Why: Applying theoretical knowledge through project-based challenges is the most effective way to validate skills for the AI engineering field.
4. Apply: Transition into professional opportunities.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet.
PASS: Grounding: all path titles are in the retrieved set
PASS: Structure: all four stages are present; empty stages are explicitly printed as none
PASS: No invented opportunities: Apply says no internships/jobs are available and names none
PASS: Source label: Source: Gemini (verified against retrieved data)

=== Cloud career changer consistency run ===
PASS: Gemini consistency: title overlap 100.0% (Jaccard; threshold 70%)
Second run source: Source: Gemini (verified against retrieved data)
Consistency overlap: PASS: title overlap 100.0% (Jaccard; threshold 70%)

=== Final summary ===
Total checks: 41
Passed: 41
Failed: 0
Pass rate: 100.0%
Paths from Gemini: 6
Paths from fallback: 0
Consistency overlap: PASS: title overlap 100.0% (Jaccard; threshold 70%)
```


---

# RAG Reliability Evaluation

- Command: `python scripts/evaluate_reliability.py --offline`
- Date: 2026-11-14

```text
Command: python scripts/evaluate_reliability.py --offline
Date: 2026-11-14
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
PASS: Source label: Source: rule-based fallback (reason: offline mode)

=== Final summary ===
Total checks: 40
Passed: 40
Failed: 0
Pass rate: 100.0%
Paths from Gemini: 0
Paths from fallback: 5
Consistency overlap: Not run (offline mode)
```
