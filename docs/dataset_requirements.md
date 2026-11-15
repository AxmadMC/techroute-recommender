# TechRoute Recommender: Dataset Requirements

| | |
|---|---|
| **Status** | Specification v1 (approved for build). Dataset not yet created |
| **Target file** | `data/opportunities.csv` |
| **Replaces** | `data/songs.csv` (Music Recommender) |
| **Last updated** | 2026-11-14 |

## Purpose

TechRoute Recommender grew out of the Music Recommender in this repository. It keeps the same content-based design: every item is a row of features, a weighted score compares those features with a user profile, and items are ranked by score. Instead of songs, it recommends free, beginner-friendly technology career resources.

This document defines what goes into `data/opportunities.csv`: the columns, allowed values, rules for including a row, coverage targets and the verification process. Every row in the dataset must follow it.

## 1. Design principles

1. **Free first.** Courses, programs and projects must be free or have a meaningful free tier. Paid items are allowed only for certification exams.
2. **Beginner-friendly.** Most rows serve beginners. Intermediate rows exist as next steps.
3. **Realistic paths.** Every track goes from a career overview to free learning, then a credential, then hands-on experience.
4. **Verified, not generated.** Every row is checked by a person against the official source before it goes into the dataset.
5. **Honest about eligibility.** Restrictions (students only, US only, needs a credit card) are recorded so users aren't misled.

## 2. Schema

The CSV has 18 columns, in this exact order:

```
id,title,provider,category,career_track,format,difficulty,hours_required,cost_type,cost_usd,remote,career_value,skills,eligibility,leads_to,description,url,last_verified
```

| # | Column | Type | Required | Rule / allowed values | Used in scoring |
|---|---|---|---|---|---|
| 1 | `id` | int | Yes | Unique, sequential | No |
| 2 | `title` | str | Yes | No commas | No (shown) |
| 3 | `provider` | str | Yes | Organization name; `Self-directed` for home labs | No (shown) |
| 4 | `category` | enum | Yes | See §3.1 | Filter |
| 5 | `career_track` | enum | Yes | See §3.2 | Yes |
| 6 | `format` | enum | No | See §3.3; blank for `career` rows | Yes |
| 7 | `difficulty` | float 0–1 | Yes | Rubric in §4.1 | Yes |
| 8 | `hours_required` | float | No | Provider's own estimate of total hours | Yes |
| 9 | `cost_type` | enum | Yes | See §3.4 | Yes |
| 10 | `cost_usd` | float | Yes | `0` for `free`; exam, parts or enrollment cost otherwise | No (shown) |
| 11 | `remote` | bool | Yes | `true` / `false` | Yes |
| 12 | `career_value` | float 0–1 | Yes | Rubric in §4.2 | Tie-breaker only |
| 13 | `skills` | str | Yes | Tags separated by semicolons (§4.3) | Yes |
| 14 | `eligibility` | str | No | Tags separated by semicolons (§3.5); blank means open to anyone | No (shown) |
| 15 | `leads_to` | str | Yes | The certification, experience or role this row leads to | No (shown) |
| 16 | `description` | str | Yes | One sentence, no commas | No (shown) |
| 17 | `url` | str | Yes | Official page. Self-directed rows link to the main free tool or guide | No (shown) |
| 18 | `last_verified` | date | Yes | `YYYY-MM-DD` of the last check by a person | No |

**Formatting rules**
- No commas in any text field, so the file needs no CSV quoting.
- A blank cell means "unknown or not applicable." The scorer skips blank fields; it never treats them as 0.
- Use lowercase values for every allowed-value column, and `true` / `false` for booleans.

## 3. Allowed values

### 3.1 `category`
| Value | Meaning |
|---|---|
| `career` | Overview of a career direction (roadmap or occupation profile) |
| `course` | Free self-contained learning content |
| `certification` | A credential: free certifications, or exams with free prep |
| `program` | Structured cohort, community or training program |
| `project` | Portfolio project or home lab |
| `internship` | Ongoing internship resource or recurring internship program |
| `volunteer` | Volunteer platform or recurring volunteer role |

### 3.2 `career_track`
`it_support` · `networking` · `cybersecurity` · `software_engineering` · `web_development` · `ai_engineering` · `cloud_computing` · `hardware_repair` · `general`

`general` is for resources useful on every track (e.g. GitHub Skills, Catchafire). The scorer gives it half track credit.

### 3.3 `format`
| Value | Meaning |
|---|---|
| `self_paced` | Learn on your own schedule |
| `cohort` | Fixed start date, learning with a group |
| `project_based` | Learn by building |
| `mentored` | Guided by a mentor or instructor |
| `work_based` | Real work for a real organization |

### 3.4 `cost_type`
| Value | Meaning |
|---|---|
| `free` | Everything needed is free |
| `freemium` | Core learning is free; an exam, certificate, upgrade or subscription costs money, or financial aid is available |
| `paid` | Must pay to take part. Allowed only for certification exams and hardware home labs (§6) |

### 3.5 `eligibility` tags
| Tag | Meaning |
|---|---|
| `college_students` | Must be enrolled in college or university |
| `students` | Any verified student |
| `recent_grads` | Recent graduates |
| `age_18_plus` | Minimum age 18 |
| `us_only` | US residents only |
| `underrepresented_in_tech` | For groups underrepresented in tech |
| `library_card` | Needs a card from a participating public library |
| `credit_card_required` | Free tier, but signing up needs a credit card |
| `macos_required` | Needs a Mac (e.g. iOS development) |
| `partner_institution` | Only through a partner school or academy |
| `prior_experience` | Expects earlier coursework or experience |

## 4. Rubrics for judgment-based fields

### 4.1 `difficulty`
| Value | Level | Meaning |
|---|---|---|
| 0.1 | Absolute beginner | No prerequisites |
| 0.2–0.3 | Beginner | Basic computer skills or one intro course |
| 0.4–0.5 | Intermediate | Needs one or more earlier courses in the track |
| 0.6–0.7 | Upper intermediate | Needs hands-on experience or a foundational certification |
| 0.8+ | Advanced | Professional experience expected (rare in this dataset) |

### 4.2 `career_value` (tie-breaker only)
| Value | Meaning |
|---|---|
| 0.9 | Industry certification often listed in job postings (e.g. CompTIA A+, Security+) |
| 0.7 | Credential or program from a major company or university, or a selective program |
| 0.5 | Completion badge, free certificate or solid portfolio piece |
| 0.3 | Learning resource with no credential |

### 4.3 `skills` tags
- Lowercase, with underscores instead of spaces: `linux`, `ip_addressing`, `security_fundamentals`.
- 2–5 tags per row.
- Home labs always include the tag `home_lab`.
- Reuse existing tags before inventing new ones. They're compared with the user's `interests`.

## 5. How the dataset feeds the scoring

The dataset is built for this formula, which keeps the Music Recommender's structure:

```
score = 2.0 × track_match        (was genre match)
      + 1.0 × format_match       (was mood match)
      + 1.0 × difficulty_fit     (was energy similarity: 1 − |skill_level − difficulty|)
      + 1.0 × free_priority      (was acoustic bonus: free = 1.0, freemium = 0.5, paid = 0)
      + 0.5 × remote_match
      + 0.5 × time_fit           (min(1, max_hours / hours_required))
      + 0.5 × interest_overlap   (share of the user's interests found in skills)
                                   maximum = 6.5
```

Ties are broken by: free before freemium before paid, then higher `career_value`, then lower `id`.

| `songs.csv` column | `opportunities.csv` column |
|---|---|
| `id`, `title` | `id`, `title` |
| `artist` | `provider` |
| `genre` | `career_track` |
| `mood` | `format` |
| `energy` | `difficulty` |
| `tempo_bpm` | `hours_required` |
| `acousticness` | `cost_type` |
| `valence` | `career_value` |
| `danceability` | (dropped) |
| (new) | `category`, `cost_usd`, `remote`, `skills`, `eligibility`, `leads_to`, `description`, `url`, `last_verified` |

## 6. Rules for including a row

1. **Free core content.** `course`, `program` and `project` rows must be `free` or `freemium`. A free tier is meaningful only if a beginner can finish the core learning content without paying. If only a teaser is free, leave the row out.
2. **Paid exams need free prep.** A `paid` certification row is allowed only if the dataset also has a free prep row whose `leads_to` names that exam.
3. **Paid home labs.** A home lab that needs hardware is `paid` with an estimated `cost_usd`. Software-only labs are `free`.
4. **Ongoing resources only.** Internships and volunteering are platforms or recurring programs, never individual postings.
5. **Official sources.** Every field comes from the provider's official page, not from aggregator sites or AI-generated text.
6. **Leads somewhere.** Every row has a `leads_to` value: an internship, volunteer experience, a certification, a job, or the next row on the path.

## 7. Coverage plan

Cost is `free` unless marked otherwise. Rows marked *(verify)* are on the watchlist in §10.

**Career-row sources.** roadmap.sh where it has a roadmap. Otherwise the US Bureau of Labor Statistics Occupational Outlook Handbook (BLS OOH), which is US-only.

### IT Support (8)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| Computer Support Specialist | BLS OOH | career | | | Help desk and IT support roles |
| Google IT Support Professional Certificate | Google (Coursera) | certification | freemium | Financial aid by application | Entry-level IT jobs; A+ prep |
| CompTIA A+ Core 2 videos | Professor Messer | course | | | CompTIA A+ |
| Linux Essentials | Cisco NetAcad | course | | | Linux admin skills |
| CompTIA A+ | CompTIA | certification | paid | | Help desk roles |
| Per Scholas IT Support | Per Scholas | program | | `us_only;age_18_plus` *(verify)* | A+ and job placement |
| Home lab: Windows and Linux VMs in VirtualBox | Self-directed | project | | | Troubleshooting experience |
| Home lab: help desk ticketing and Active Directory users | Self-directed | project | | | Help desk interview stories |

### Networking (8)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| Network and Computer Systems Administrator | BLS OOH | career | | | Network admin roles |
| Networking Basics | Cisco Skills for All | course | | | CCNA path |
| Networking Devices and Initial Configuration | Cisco Skills for All | course | | | CCNA path |
| Getting Started with Cisco Packet Tracer | Cisco Skills for All | course | | NetAcad account | Packet Tracer labs |
| CompTIA Network+ videos | Professor Messer | course | | | CompTIA Network+ |
| CompTIA Network+ | CompTIA | certification | paid | | Network technician roles |
| Home lab: small-office network in Packet Tracer | Self-directed | project | | | VLAN, DHCP and routing experience |
| Home lab: packet capture with Wireshark | Self-directed | project | | | Traffic analysis skills |

### Cybersecurity (13)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| Cybersecurity roadmap | roadmap.sh | career | | | Security analyst roles |
| Introduction to Cybersecurity | Cisco Skills for All | course | | | Junior Cybersecurity Analyst |
| Junior Cybersecurity Analyst career path | Cisco Skills for All | course | | | Cisco CCST Cybersecurity *(verify)* |
| CS50 Cybersecurity | Harvard | course | | | Security fundamentals |
| Pre Security | TryHackMe | course | freemium | | Cyber Security 101 |
| Intro to Cyber Security / Cyber Security 101 | TryHackMe | course | freemium | | SOC roles |
| CompTIA Security+ videos | Professor Messer | course | | | CompTIA Security+ |
| Security, Compliance and Identity Fundamentals (SC-900) | Microsoft | certification | freemium | | Entry-level security credential |
| CompTIA Security+ | CompTIA | certification | paid | | SOC analyst roles |
| Intro to Cybersecurity (CYB101) | CodePath | program | | `college_students` | CYB102 |
| Intermediate Cybersecurity (CYB102) | CodePath | program | | `college_students` | Security internships |
| OverTheWire Bandit | OverTheWire | project | | | Linux and command-line skills |
| Home lab: SIEM with Wazuh or Security Onion | Self-directed | project | | | SOC analyst skills |

*Conditional:* SOC Level 1 (TryHackMe). Include it only if checking shows a meaningful free tier (rule 6.1).

### Software Engineering (12)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| Backend / Software Developer | roadmap.sh | career | | | Software engineering roles |
| CS50x | Harvard | course | | | Free CS50 certificate |
| CS50P | Harvard | course | | | Python skills |
| Technical Interview Prep (TIP) | CodePath | program | | `college_students` | SWE internships |
| Mock Interview Prep | CodePath | program | | `college_students` | Interview readiness |
| Android Development | CodePath | program | | `college_students` | Mobile internships |
| iOS Development | CodePath | program | | `college_students;macos_required` | Mobile internships |
| CS50x final project | Harvard | project | | | Portfolio piece |
| Backend project ideas | roadmap.sh | project | | | Portfolio APIs |
| Outreachy internships | Outreachy | internship | | `underrepresented_in_tech` | Paid open-source experience |
| MLH Fellowship | Major League Hacking | internship | | `age_18_plus` *(verify)* | Open-source experience |
| Open-source contributions (good first issues) | GitHub | volunteer | | | Real-world code reviews |

### Web Development (8)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| Frontend Developer | roadmap.sh | career | | | Web developer roles |
| Responsive Web Design | freeCodeCamp | certification | | | Free certification |
| JavaScript Algorithms and Data Structures | freeCodeCamp | certification | | | Free certification |
| Back End Development and APIs | freeCodeCamp | certification | | | Free certification |
| Web Development (WEB101/102) | CodePath | program | | `college_students` | Web internships |
| Portfolio site on GitHub Pages | GitHub | project | | | Portfolio hub |
| Frontend project ideas | roadmap.sh | project | | | Portfolio pieces |
| Contribute to freeCodeCamp | freeCodeCamp | volunteer | | | Open-source experience |

### AI Engineering / Applied AI (10)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| AI Engineer | roadmap.sh | career | | | Applied AI roles |
| CS50 AI | Harvard | course | | | AI and ML foundations |
| Data Analysis with Python | freeCodeCamp | certification | | | Free certification |
| Machine Learning with Python | freeCodeCamp | certification | | | Free certification |
| Kaggle Learn (Python, Pandas, Intro to ML) | Kaggle | course | | | Kaggle competitions |
| Introduction to Generative AI | Google Cloud Skills Boost | course | | | GenAI skill badge |
| Azure AI Fundamentals (AI-900) | Microsoft | certification | freemium | | Entry-level AI credential |
| AI Engineering | CodePath | program | | `college_students` | AI internships |
| Titanic competition | Kaggle | project | | | First ML portfolio piece |
| Applied AI app (retrieval-based Q&A with a local model) | Self-directed | project | | | Applied AI portfolio piece |

### Cloud Computing (12)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| DevOps / Cloud Engineer | roadmap.sh | career | | | Cloud roles |
| AZ-900 learning paths | Microsoft Learn | course | | | AZ-900 |
| AZ-104 learning paths | Microsoft Learn | course | | `prior_experience` | AZ-104 (intermediate) |
| AWS Cloud Practitioner Essentials | AWS Skill Builder | course | | | AWS Cloud Practitioner exam |
| AWS Cloud Quest (Cloud Practitioner role) | AWS | course | freemium | | Hands-on AWS labs |
| AWS Educate | AWS | program | | Age limit *(verify)* | Badges and job board |
| Google Cloud Skills Boost (no-cost labs) | Google Cloud | course | freemium | | Skill badges |
| Azure Fundamentals (AZ-900) | Microsoft | certification | freemium | | Cloud support roles |
| AWS Certified Cloud Practitioner | AWS | certification | freemium | | Cloud support roles |
| Cloud Engineering | CodePath | program | | `college_students` | Cloud internships |
| Cloud Resume Challenge | Cloud Resume Challenge | project | | `credit_card_required` | Well-known cloud portfolio project |
| Home lab: static site on AWS or Azure free tier | Self-directed | project | | `credit_card_required` | Deployment experience |

### Hardware / Computer Repair (8)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| Computer repair technician | BLS OOH *(verify title)* | career | | | Bench and field technician roles |
| CompTIA A+ Core 1 videos | Professor Messer | course | | | CompTIA A+ |
| Computer Hardware Basics | Cisco Skills for All *(verify)* | course | | | IT Essentials |
| Repair guides | iFixit | course | | | Repair skills |
| IT Essentials | Cisco NetAcad | program | | `partner_institution` | A+ prep |
| Home lab: build or upgrade a PC | Self-directed | project | paid (parts) | | Hands-on hardware experience |
| Home lab: refurbish an old laptop with Linux | Self-directed | project | | Needs a spare device | Repair portfolio story |
| Volunteer fixer | Repair Café | volunteer | | In person (`remote=false`) | Customer-facing repair experience |

### General, across all tracks (8)
| Title | Provider | Category | Cost | Eligibility | Leads to |
|---|---|---|---|---|---|
| GitHub Skills courses | GitHub | course | | | Git fluency |
| LinkedIn Learning via public library | LinkedIn | course | freemium | `library_card` | Course certificates |
| Power Platform Fundamentals (PL-900 path) | Microsoft Learn | course | | | PL-900 |
| GitHub Student Developer Pack | GitHub | program | | `students` | Free developer tools |
| Global Hack Week and hackathons | Major League Hacking | program | | | Projects and networking |
| Micro-internships | Parker Dewey | internship | | `college_students;recent_grads` | Paid short projects |
| Internship search | LinkedIn | internship | | | Internships |
| Skills-based volunteering | Catchafire | volunteer | | Some projects need `prior_experience` | Nonprofit project experience |

## 8. Size and balance targets

| | IT | Net | Cyber | SWE | Web | AI | Cloud | HW | Gen | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|
| Planned rows | 8 | 8 | 13 | 12 | 8 | 10 | 12 | 8 | 8 | **87** |

| Target | Requirement |
|---|---|
| Dataset size | 85–90 rows |
| Rows per track | At least 8 and at most 13. Each track has at least 1 career row, at least 1 free course, and at least 1 project or home lab |
| Cost mix | `free` ≥ 75% · `freemium` ≤ 20% · `paid` ≤ 10% (planned: ~82 / ~13 / ~5%) |
| Difficulty | ≥ 70% of rows at `difficulty` ≤ 0.3 |
| Format variety | Every `format` value appears in at least 5 rows |

**Known imbalance.** Cybersecurity, software engineering and cloud have more rows because most required providers fall in those tracks. Users who pick a track aren't affected, since track match decides the ranking. Undecided users will see those tracks more often; this is documented as a limitation in the model card.

## 9. Collection and verification process

1. **List candidates.** Fill the §7 tables with title, provider and URL only.
2. **Fill objective fields** (`cost_type`, `cost_usd`, `hours_required`, `remote`, `format`, `eligibility`) from the official page.
3. **Score the judgment-based fields** (`difficulty`, `career_value`) using the rubrics in §4.
4. **Verify by hand.** A person opens every URL, confirms the page, cost and eligibility, then sets `last_verified`. A row without `last_verified` doesn't go into the dataset.
5. **Check the whole file before committing:**
   - [ ] Columns and their order match §2 exactly
   - [ ] Every allowed-value field uses a value from §3
   - [ ] `difficulty` and `career_value` are within 0–1
   - [ ] `cost_usd` is 0 for every `free` row
   - [ ] Every `paid` certification has a free prep row that leads to it (§6.2)
   - [ ] IDs are unique and no text field has a comma
   - [ ] The §8 balance targets are met
6. **Re-verify.** Re-check every row before submission or a demo. Rows not checked in 90 days count as stale.

**Effort estimate:** about 87 rows at roughly 5 minutes each, around 7 hours.

## 10. Verification watchlist

These items are the most likely to have changed since this spec was drafted. Check them first.

| Item | What to check |
|---|---|
| Cisco Skills for All | Content may have moved onto `netacad.com`; confirm the URLs. Confirm "Computer Hardware Basics" exists, and which exam Junior Cybersecurity Analyst prepares for |
| TryHackMe | Whether "Intro to Cyber Security" was replaced by "Cyber Security 101"; how much of SOC Level 1 is free |
| Microsoft certifications | AZ-900, AZ-104, SC-900, AI-900 and PL-900 are still offered, and their current exam prices |
| CompTIA | A+ moved to a new exam series in 2025. Confirm Professor Messer's videos match the current exam versions, and the exam prices |
| freeCodeCamp | The curriculum was reorganized; certification names and URLs may now be listed as legacy |
| AWS | Only the Cloud Practitioner role in Cloud Quest is free; AWS Educate eligibility and age rules |
| CodePath | Exact course names (Mock Interview Prep, Cloud Engineering, AI Engineering) and eligibility |
| MLH Fellowship | Still running, and its eligibility |
| BLS OOH | Exact occupation title for computer repair |
| Per Scholas | Eligibility rules by location |

## 11. Example rows (format only)

> ⚠️ These rows show the formatting only. Their values have **not** been verified. Don't copy them into `opportunities.csv` without completing §9.

```csv
id,title,provider,category,career_track,format,difficulty,hours_required,cost_type,cost_usd,remote,career_value,skills,eligibility,leads_to,description,url,last_verified
1,Responsive Web Design,freeCodeCamp,certification,web_development,project_based,0.1,300,free,0,true,0.5,html;css;accessibility,,Free certification,Free certification earned by building five projects.,https://www.freecodecamp.org/learn/2022/responsive-web-design/,
2,CompTIA Security+ videos,Professor Messer,course,cybersecurity,self_paced,0.4,,free,0,true,0.3,security_fundamentals;threats;cryptography,prior_experience,CompTIA Security+,Free video course covering every Security+ exam objective.,https://www.professormesser.com/,
3,CompTIA Security+,CompTIA,certification,cybersecurity,self_paced,0.4,,paid,425,true,0.9,security_fundamentals;threats;cryptography,,SOC analyst roles,Widely requested entry-level security certification.,https://www.comptia.org/certifications/security,
4,Home lab: Windows and Linux VMs in VirtualBox,Self-directed,project,it_support,project_based,0.2,10,free,0,true,0.5,virtualization;windows;linux;home_lab,,Troubleshooting experience,Build a two-VM lab to practice installs and troubleshooting.,https://www.virtualbox.org/,
5,Outreachy internships,Outreachy,internship,software_engineering,mentored,0.4,,free,0,true,0.8,open_source;git,underrepresented_in_tech,Paid open-source experience,Paid remote open-source internships with mentors.,https://www.outreachy.org/,
```

## 12. Decisions log

| Decision | Rationale |
|---|---|
| Single CSV with a `category` column | One scoring function handles all 7 categories, as `songs.csv` did |
| `ai_ml` renamed to `ai_engineering` | Matches the Applied AI focus |
| `data_analytics` folded into `ai_engineering` | Not in the required track list. Its resources (freeCodeCamp Data Analysis, Kaggle Learn) are AI foundations. Can be split back out if ~8 more rows are added |
| `networking` and `hardware_repair` added | Required coverage areas with distinct career paths |
| `eligibility` and `leads_to` added, display-only | Shows restrictions and next steps without changing the scoring formula |
| `general` track gets half track credit | Lets cross-track resources (internships, volunteering) reach every user |
| Remote is a +0.5 bonus, not a filter | Kept simple for V1; may become a filter later |
| Internships and volunteering are ongoing resources | Individual postings expire within weeks |
| BLS OOH used for career rows without a roadmap.sh roadmap | Free, authoritative pay and outlook data (US-centric limitation noted) |

## 13. Origin and AI use

This specification was drafted together with an AI coding assistant (Claude Code) during the TechRoute planning sessions:
1. Codebase analysis and migration plan.
2. Opportunity data model and scoring design.
3. Initial dataset design.
4. Expanded provider and track requirements.

The person who built this project chose the providers, tracks and priorities. The AI proposed the schema, allowed values, rubrics, coverage plan and verification process. The AI didn't verify any provider name, URL, price or eligibility rule online; that's why every row must pass human verification (§9) and why §10 exists.

See `ai_interactions.md` for the full log of AI interactions.
