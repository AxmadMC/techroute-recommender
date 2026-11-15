# TechRoute Recommender Model Card

## 1. Model Overview

- **Name:** TechRoute Recommender
- **Version/date:** Repository snapshot dated 2026-11-14; no software version tag is declared.
- **Developer:** Ahmed Ali, Web Developer.
- **Base project:** Project 3: Music Recommender Simulation (CodePath AI110).

I use a rule-based recommender to score and rank rows in `data/opportunities.csv`, with remote and prerequisite guardrails. Gemini, using `gemini-3.1-flash-lite` by default, generates a four-stage learning path from retrieved items only. The app parses and verifies the response against retrieved opportunity titles; if no key is available, a call fails, output is rejected, or offline mode is selected, it uses a rule-based fallback with a source label and reason.

## 2. Intended Use and Non-Intended Use

**Intended use:** I built TechRoute for students and career changers exploring free or low-cost learning routes into technology career tracks.

**Not intended:** This tool does not guarantee a career outcome and is not hiring, admissions, or financial advice. It is not a replacement for career advisors, instructors, or mentors.

## 3. Data

I manually curated 87 opportunity rows across nine tracks: IT Support, Networking, Cybersecurity, Software Engineering, Web Development, AI Engineering, Cloud Computing, Hardware Repair, and General.

All 87 `last_verified` cells are blank, so the dataset does not record verification dates.

Internship and job coverage is limited:

- Software Engineering: 2 internship rows, 0 job rows.
- General: 2 internship rows, 0 job rows.
- IT Support, Networking, Cybersecurity, Web Development, AI Engineering, Cloud Computing, and Hardware Repair: 0 internship rows and 0 job rows.
- There are no job rows in the dataset.

## 4. Limitations and Biases

- **Single-curator selection:** I assembled the dataset, so its coverage reflects my knowledge and choices. It is English-language, includes US-oriented programs, and gives substantial representation to well-known providers. For example, CodePath and Self-directed each appear in 9 rows; roadmap.sh appears in 7; Cisco Skills for All, Microsoft Learn, and freeCodeCamp each appear in 6.
- **Coverage gaps:** Seven of the nine tracks have no internship or job rows. For those tracks, the Apply step cannot recommend a dataset opportunity.
- **Filter-bubble effect:** The inherited track-match weight is +2.0, which is higher than any other individual scoring factor. This tends to favor the selected track over adjacent tracks; General resources receive partial track credit.
- **Hand-tuned scoring:** The weights were chosen by me, not learned from recommendation outcomes. `skill_level` is self-reported.
- **Free and remote preferences:** All six presets prefer free resources and require remote options. This can under-represent paid or in-person opportunities for users who might consider them.
- **Ties and near-duplicates:** Four Cybersecurity recommendations tied at exactly 5.57 in the saved reliability run. The dataset also contains near-duplicate Azure entries, “AZ-900 learning paths” and “Azure Fundamentals AZ-900.”
- **Path overload and brand preference:** Gemini may favor recognizable providers or group more resources into a stage than a student can reasonably complete. In the saved AI Engineering sample, a 12-hour-per-week profile receives a Build Skills stage containing four items, including “Data Analysis with Python” and “Machine Learning with Python,” each listed in the dataset as a 300-hour certification. `max_hours` affects ranking as a soft bonus; it does not cap total path hours.
- **Stale data risk:** Links, costs, and eligibility can change. The blank `last_verified` values mean I cannot use this field to show when the entries were last checked.
- **External processing:** When a Gemini key is used, allowlisted learning preferences and retrieved opportunity details are sent to Google's Gemini API.

## 5. Misuse and Prevention

- **Over-reliance on career recommendations:** A user could treat the result as authoritative advice. The CLI shows recommendation score explanations and labels whether the path came from Gemini or the fallback; this model card documents limitations. Neither mechanism guarantees that a path is right for an individual.
- **Prompt injection through interests:** The profile validator keeps supported fields and constrains interest strings to a short character pattern, but it does not semantically check them for instructions. The prompt includes the allowlisted interests. Output verification checks the response structure and opportunity titles; it does not content-check free-text `goal` or `why` explanations. Content checks for those explanations are future work.
- **Dataset poisoning:** The CSV loader checks data types and certain values, but does not detect malicious links or validate the provenance of each row. I rely on human curation; dataset changes should be reviewed before they are accepted.
- **API key exposure:** `.env` is in `.gitignore`, `.env.example` contains placeholders, and the application does not print or log the API key. A test checks that the key does not appear in the log.
- **Personal data:** The CLI uses learning-preference presets, not login or identity fields. Unexpected profile keys are dropped before prompt construction, and runtime profiles and generated paths are not saved. Logs may contain operational metadata such as target track, counts, and reasons, but do not include the full profile, prompt, or AI response.

## 6. Testing and Reliability Results

I have 30 unit tests; Gemini behavior is mocked, so the test suite does not call the real API. The saved reliability evaluation covers five profiles: online, 41/41 checks passed (100%); offline, 40/40 passed (100%). The two Cloud career changer Gemini paths had 100% title overlap under the evaluator's Jaccard comparison.

Human evaluation by Ahmed Ali: five Gemini profiles are marked Pass across the scored columns; AI Engineering is marked Pass overall, with `v` entered for no invented/off-topic. The offline Cybersecurity route is Partial for beginner order and Overall, and Pass for the other scored columns. See [assets/human_evaluation.md](assets/human_evaluation.md).

| Check name | What it verifies | Result |
|---|---|---|
| Track relevance | At least four of the top five recommendations match the target track. | Pass online and offline |
| Remote guardrail | No non-remote result is returned when remote is required. | Pass online and offline |
| Prerequisite guardrail | A low-skill user's first-ranked item is not tagged `prior_experience`. | Pass online and offline |
| Result count | Five results are returned, or a shortfall is clearly reported. | Pass online and offline |
| Grounding | Every generated opportunity title exists in the retrieved set. | Pass online and offline |
| Structure | The four stages exist, with empty stages clearly represented. | Pass online and offline |
| No invented opportunities | If no internship or job is retrieved, Apply says so and names none. | Pass online and offline |
| Source label | The path states Gemini verification or a fallback reason. | Pass online and offline |
| Gemini consistency | The two Cloud career changer paths have at least 70% title overlap. | Pass online at 100%; not run offline |

Before the prerequisite penalty, AZ-104 learning paths ranked #2 for the Cloud career changer. The dataset marks that item `prior_experience`; after the penalty, it left the Cloud career changer's top five.

These checks were designed after I observed the recommender. A 100% pass rate shows that the implemented checks passed on these profiles; it does not establish general real-world quality.

Reports: [assets/evaluation_results.md](assets/evaluation_results.md), [assets/sample_runs.md](assets/sample_runs.md), and [assets/human_evaluation.md](assets/human_evaluation.md).

## 7. What Surprised Me During Reliability Testing

- `prefers_free` was accepted as input but initially had no effect on scores. Testing exposed the gap, and I corrected the scoring behavior.
- AZ-104, which requires prior experience, ranked #2 for a career changer before I added the prerequisite penalty.
- Four Cybersecurity items tied at exactly 5.57.
- In the runs I reviewed, Gemini's path was more noticeably ordered than my rule-based fallback; it placed projects in Prove Skills.
- Gemini reported that there were no internships in the dataset rather than inventing them. Empty Apply steps revealed a dataset gap, not an AI failure.
- My first Gemini runs failed because of setup issues, including an incorrect run command and missing dependencies, rather than because of the model's recommendations.

## 8. Collaboration with AI

I used Claude to plan the project as small numbered tasks and write precise prompts. I used GitHub Copilot in VS Code to implement tasks, show proposed changes before applying them, and run tests. I reviewed changes, ran the app, and committed after each task.

I accepted Copilot's suggestion to implement the RAG feature with mocked Gemini tests and a no-key fallback before attempting a live API run. This kept the tests independent of the live API and allowed the app to generate a path without a key.

I narrowed some proposed constraints: `needs_remote` became a hard filter; `prefers_free` turns off the free bonus but does not hide paid options; and `prior_experience` items receive a soft -1.0 penalty instead of being removed. I made these choices so beginners can still see possible next steps.

An AI assistant drafted an architecture diagram before the system was finished. I set it aside and had the diagram regenerated from the final code later. I also deferred diversity rules and a hard `max_hours` limit as out of scope.

## 9. Future Improvements

- Add internship and job rows for every track, deduplicate entries, and fill in `last_verified` dates.
- Add diversity rules for top results and consider an optional hard `max_hours` limit.
- Add content checks for AI-written explanations and confidence scoring.
- Collect anonymous, opt-in feedback to tune the scoring weights.
