# RAG Enhancement Comparison

- Command: `python scripts/compare_rag.py`
- Date: 2026-11-15
- Model: `gemini-3.1-flash-lite`

The before run invokes the CLI with `--no-guides`; the after run uses the track guide. Skill-term cells show matched/available core-skill terms and the average Why length in words.

| Profile | Before skill terms | After skill terms | Before/after verification | Repairs |
| --- | --- | --- | --- | --- |
| cloud_career_changer | 0/9 (Why avg 15.8 words) | 0/9 (Why avg 21.2 words) | Pass / Pass | 0 / 0 |
| networking_student | 0/8 (Why avg 16.5 words) | 1/8 (Why avg 17.8 words) | Pass / Pass | 0 / 0 |
| ai_engineering_student | 1/9 (Why avg 18.5 words) | 2/9 (Why avg 26.2 words) | Pass / Pass | 0 / 0 |

## cloud_career_changer — before

Command: `python -m src.main --profile cloud_career_changer --no-guides`

```text
Source: Gemini (verified against retrieved data)
1. Foundations: Gain a baseline understanding of core cloud computing concepts and terminology.
   Opportunities: AZ-900 learning paths, AWS Cloud Practitioner Essentials
   Why: These introductory resources provide the necessary conceptual framework for understanding cloud infrastructure and services.
2. Build Skills: Develop technical competencies through structured cloud computing programs.
   Opportunities: Cloud Engineering, AWS Educate
   Why: Engaging in structured programs helps transition from theoretical knowledge to practical skill sets in cloud environments.
3. Prove Skills: Demonstrate proficiency by executing a tangible, hands-on cloud project.
   Opportunities: Home lab: static site on AWS or Azure free tier, Google Cloud Skills Boost no cost labs
   Why: Applying knowledge in a practical project environment validates learning and improves technical confidence.
4. Apply: Validate your cloud expertise with industry-recognized certifications.
   Opportunities: none
   Why: Obtaining certifications demonstrates professional competence in cloud domains. Note: There are no internship or job opportunities in the dataset yet.
```

## cloud_career_changer — after

Command: `python -m src.main --profile cloud_career_changer`

```text
Source: Gemini (verified against retrieved data)
1. Foundations: Gain a baseline understanding of cloud computing models, service terminology, and the shared-responsibility framework.
   Opportunities: AZ-900 learning paths, AWS Cloud Practitioner Essentials
   Why: These foundational resources introduce the core concepts of cloud services, identity, and security that are essential for cloud computing practitioners.
2. Build Skills: Acquire hands-on experience by deploying isolated environments and practicing cloud resource configuration.
   Opportunities: AWS Educate, Google Cloud Skills Boost no cost labs
   Why: Practical lab environments allow you to safely build, configure, and manage cloud resources to reinforce theoretical knowledge.
3. Prove Skills: Demonstrate technical competency by implementing and documenting a cloud-based project from start to finish.
   Opportunities: Home lab: static site on AWS or Azure free tier
   Why: Creating a personal project provides evidence of your ability to deploy, manage, and clean up cloud resources in a professional manner.
4. Apply: Prepare for real-world professional environments by refining your portfolio and assessing alignment with technical roles.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet, but you can leverage existing certifications and program credentials to validate your skills for potential future roles.
```

## networking_student — before

Command: `python -m src.main --profile networking_student --no-guides`

```text
Source: Gemini (verified against retrieved data)
1. Foundations: Gain an introductory understanding of networking concepts and terminology.
   Opportunities: Networking Basics, CompTIA Network+ videos
   Why: These foundational resources provide the essential knowledge base required to understand how networking and IP addressing work.
2. Build Skills: Develop technical proficiency in configuring and managing network environments.
   Opportunities: Getting Started with Cisco Packet Tracer, Networking Devices and Initial Configuration
   Why: These resources build practical skills in using industry-standard simulation tools and configuring network hardware.
3. Prove Skills: Apply networking theory and simulation skills to real-world technical scenarios.
   Opportunities: Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
   Why: Project-based work confirms your ability to design networks and analyze traffic flow in a controlled environment.
4. Apply: Understand professional career paths and expectations in the networking field.
   Opportunities: none
   Why: Reviewing professional roles provides insight into industry standards; however, no internship or job opportunities are in the dataset yet.
```

## networking_student — after

Command: `python -m src.main --profile networking_student`

```text
Source: Gemini (verified against retrieved data)
1. Foundations: Gain a solid understanding of how network components interact and communicate to establish a baseline for networking.
   Opportunities: Networking Basics
   Why: Establishing core knowledge of protocols, addressing, and hardware is essential before practicing network configurations.
2. Build Skills: Develop practical proficiency in configuring networking equipment within a virtualized environment.
   Opportunities: Getting Started with Cisco Packet Tracer, Networking Devices and Initial Configuration
   Why: Hands-on experience with simulation tools is necessary to bridge the gap between theoretical knowledge and practical device setup.
3. Prove Skills: Demonstrate the ability to design networks and analyze traffic flow to verify connectivity.
   Opportunities: Home lab: small-office network in Packet Tracer, Home lab: packet capture with Wireshark
   Why: Applying skills to real-world scenarios in a lab environment proves competency in addressing and network troubleshooting.
4. Apply: Connect technical networking proficiency with professional expectations and career pathways.
   Opportunities: none
   Why: Reviewing professional profiles helps align technical skills with industry standards. Please note that no internship or job opportunities are in the dataset yet.
```

## ai_engineering_student — before

Command: `python -m src.main --profile ai_engineering_student --no-guides`

```text
Source: Gemini (verified against retrieved data)
1. Foundations: Gain a comprehensive understanding of the AI engineering landscape and the core concepts required to begin your journey.
   Opportunities: AI Engineer
   Why: Establishing a baseline understanding of the AI field provides the necessary roadmap to navigate subsequent technical learning.
2. Build Skills: Develop technical proficiency in Python programming and essential data analysis libraries to prepare for machine learning tasks.
   Opportunities: Kaggle Learn Python Pandas and Intro to Machine Learning, Data Analysis with Python
   Why: These resources build the fundamental coding and analytical skills required to manipulate data and implement machine learning models.
3. Prove Skills: Validate your machine learning knowledge through a practical, project-based evaluation.
   Opportunities: Titanic competition
   Why: Applying learned concepts to a real-world dataset helps bridge the gap between theoretical knowledge and practical execution.
4. Apply: Integrate your skills by building a functional AI application in a practical, hands-on environment.
   Opportunities: none
   Why: This final stage reinforces learning by creating a personal project; note that no internship or job opportunities are in the dataset yet.
```

## ai_engineering_student — after

Command: `python -m src.main --profile ai_engineering_student`

```text
Source: Gemini (verified against retrieved data)
1. Foundations: Establish a baseline understanding of the AI engineering roadmap and necessary core concepts.
   Opportunities: AI Engineer
   Why: This provides a structured overview of the field and the fundamental concepts required to transition from a beginner to an AI engineer.
2. Build Skills: Develop proficiency in Python data manipulation and fundamental machine learning techniques.
   Opportunities: Kaggle Learn Python Pandas and Intro to Machine Learning, Data Analysis with Python
   Why: These resources build the practical Python and data preparation skills essential for handling datasets and understanding model inputs.
3. Prove Skills: Apply machine learning fundamentals to a specific, measurable task to validate data handling and model usage skills.
   Opportunities: Titanic competition
   Why: This project offers a practical environment to apply data analysis and machine learning skills on a well-defined task with clear evaluation metrics.
4. Apply: Integrate a model into a functional application while documenting the data, model logic, and failure cases.
   Opportunities: none
   Why: No internship or job opportunities are in the dataset yet; however, this stage focuses on synthesizing programming and evaluation skills into a cohesive project. You should aim to build a project that integrates model usage into an application to demonstrate these combined capabilities.
```

Observation:
Enabling track guides improved explanation detail across all three profiles, with average explanation length increasing in each case. Skill-term matches improved for Networking (0 to 1) and AI Engineering (1 to 2), while Cloud remained unchanged at 0.

Limitation:
Skill-term coverage remained low across all profiles, showing that track guides did not substantially improve skill matching. Longer explanations do not necessarily indicate better recommendations, and testing only three profiles limits the conclusions.