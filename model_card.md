# TechRoute Recommender Model Card

## 1. Model Overview

- **Name:** TechRoute Recommender
- **Version/date:** Repository snapshot dated 2026-11-15; no software version tag is declared.
- **Developer:** Ahmed Ali, Web Developer.
- **Base project:** Project 3: Music Recommender Simulation (CodePath AI110).

I use a rule-based recommender to score and rank rows in `data/opportunities.csv`, with remote and prerequisite guardrails. The CLI and Streamlit UI share `src/pipeline.py`. When Gemini (`gemini-3.1-flash-lite` by default) is enabled, the agent plans and generates a four-stage path from retrieved opportunities, verifies its structure and titles, and can request up to two self-corrections before deciding to accept the path or use a rule-based fallback. A second retrieval source, `data/track_guides/`, provides track context for goals and explanations; guide text is not a source of opportunity titles. The UI offers the same pipeline and an in-memory PDF download.

## 2. Intended Use and Non-Intended Use

**Intended use:** I built TechRoute for students and career changers exploring free or low-cost learning routes into technology career tracks.

**Not intended:** This tool does not guarantee a career outcome and is not hiring, admissions, or financial advice. It is not a replacement for career advisors, instructors, or mentors.

## 3. Data

I manually curated 87 opportunity rows across nine tracks: IT Support, Networking, Cybersecurity, Software Engineering, Web Development, AI Engineering, Cloud Computing, Hardware Repair, and General.

All 87 `last_verified` cells are blank, so the dataset does not record verification dates.

I also curated nine short, general track guides with AI assistance, one for each target track. They contain no URLs. I reviewed the guide content; this is a single-person review, not independent validation.

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
- **Path size and brand preference:** Gemini may favor recognizable providers or group more resources into a stage than a student can reasonably complete. The verifier caps each stage at three opportunities, but paths can still be lean: in the fresh AI Engineering evaluation run, Build Skills contained only one item. `max_hours` affects ranking as a soft bonus; it does not cap total path hours.
- **Guide limitations:** The guides are AI-assisted, general-purpose content reviewed by one person, and are not independently validated. They contain no URLs and cannot verify current provider information.
- **Limited RAG metric:** The guide comparison counts exact core-skill phrases in goals and explanations, not semantic matches. It covers three profiles with one before and one after run per profile; the observed gains were small.
- **Run-to-run consistency:** An earlier evaluation reported 100% title overlap. In the latest fresh online evaluation, no overlap percentage could be calculated because one Cloud consistency path fell back after two repair attempts. The consistency check failed; this run provides no new numeric overlap.
- **Stale data risk:** Links, costs, and eligibility can change. The blank `last_verified` values mean I cannot use this field to show when the entries were last checked.
- **External processing:** When a Gemini key is used, allowlisted learning preferences and retrieved opportunity details are sent to Google's Gemini API.

## 5. Misuse and Prevention

- **Over-reliance on career recommendations:** A user could treat the result as authoritative advice. The CLI shows recommendation score explanations and labels whether the path came from Gemini or the fallback; this model card documents limitations. Neither mechanism guarantees that a path is right for an individual.
- **Prompt injection through interests:** The profile validator keeps supported fields and constrains interest strings to a short character pattern, but it does not semantically check them for instructions. The prompt includes the allowlisted interests. Output verification checks the response structure and opportunity titles; it does not content-check free-text `goal` or `why` explanations. Content checks for those explanations are future work.
- **Dataset poisoning:** The CSV loader checks data types and certain values, but does not detect malicious links or validate the provenance of each row. I rely on human curation; dataset changes should be reviewed before they are accepted.
- **API key exposure:** `.env` is in `.gitignore`, `.env.example` contains placeholders, and the application does not print or log the API key. A test checks that the key does not appear in the log.
- **Personal data:** The CLI uses learning-preference presets, not login or identity fields. Unexpected profile keys are dropped before prompt construction, and runtime profiles and generated paths are not saved. Logs may contain operational metadata such as target track, counts, and reasons, but do not include the full profile, prompt, or AI response.
- **Web UI and PDF:** The Streamlit UI has no login and does not save submitted profiles, routes, or PDFs; existing operational logs are the only app data written to disk. The PDF is built in memory and is only downloaded to the user's chosen location.

## 6. Testing and Reliability Results

The fresh `python -m pytest` run passed 52 tests. Gemini behavior is mocked; tests do not call the real API. Fresh reliability runs on 2026-11-15 evaluated all six preset profiles: online, 66/67 checks passed (98.5%); offline, 66/66 passed (100%). The latest online Jaccard consistency overlap was unavailable because one of the two Cloud paths fell back after two repair attempts; the consistency check is counted as the single online failure. Offline consistency is not run.

Human evaluation by Ahmed Ali: six Gemini profiles are marked Pass overall; the AI Engineering no-invented/off-topic cell contains `v` in the evaluator's table. The offline Cybersecurity route is Partial for beginner order and Overall, and Pass for the other scored columns. See [assets/human_evaluation.md](assets/human_evaluation.md).

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
| Agent: stage size <= 3 | No stage contains more than three opportunities. | Pass online and offline |
| Agent: no duplicate titles | A title does not appear in multiple stages. | Pass online and offline |
| Gemini consistency | The two Cloud career changer paths have at least 70% title overlap. | Online: failed; overlap unavailable after a fallback. Not run offline. |

The latest online run used zero repair attempts across its six preset-profile paths. Its separate Cloud consistency run used two repair attempts and then fell back. The offline run used no Gemini calls and no repairs.

The guide comparison's exact-term results were:

| Profile | Core-skill phrases matched (before -> after) | Average Why words (before -> after) |
|---|---:|---:|
| Cloud career changer | 0/9 -> 0/9 | 15.8 -> 21.2 |
| Networking student | 0/8 -> 1/8 | 16.5 -> 17.8 |
| AI Engineering student | 1/9 -> 2/9 | 18.5 -> 26.2 |

This comparison used three profiles and one before/after run per profile. It shows modest phrase-match gains and longer explanations, not evidence of improved recommendation quality. See [assets/rag_comparison.md](assets/rag_comparison.md).

Before the prerequisite penalty, AZ-104 learning paths ranked #2 for the Cloud career changer. The dataset marks that item `prior_experience`; after the penalty, it left the Cloud career changer's top five.

These checks were designed after I observed the recommender. The 100% offline pass rate and 98.5% online pass rate describe these profiles and checks; they do not establish general real-world quality. Online consistency was not measurable in the latest run.

Reports: [assets/evaluation_results.md](assets/evaluation_results.md), [assets/sample_runs.md](assets/sample_runs.md), [assets/agent_traces.md](assets/agent_traces.md), [assets/rag_comparison.md](assets/rag_comparison.md), and [assets/human_evaluation.md](assets/human_evaluation.md).

## 7. What Surprised Me During Reliability Testing

- `prefers_free` was accepted as input but initially had no effect on scores. Testing exposed the gap, and I corrected the scoring behavior.
- AZ-104, which requires prior experience, ranked #2 for a career changer before I added the prerequisite penalty.
- Four Cybersecurity items tied at exactly 5.57.
- In the runs I reviewed, Gemini's path was more noticeably ordered than my rule-based fallback; it placed projects in Prove Skills.
- Gemini reported that there were no internships in the dataset rather than inventing them. Empty Apply steps revealed a dataset gap, not an AI failure.
- My first Gemini runs failed because of setup issues, including an incorrect run command and missing dependencies, rather than because of the model's recommendations.
- An earlier consistency run reported 100% title overlap. The latest online checks could not calculate an overlap because a Cloud comparison path fell back after two repair attempts, so the earlier result was not reproduced.
- The latest online run did invoke two self-correction attempts for the separate Cloud consistency path, but the path still fell back; the six preset-profile runs needed no repairs. Mocked tests verify the repair loop, while this live run shows repairs may not succeed.
- The track-guide comparison showed modest exact-phrase gains: Networking improved from 0 to 1 matched core-skill phrase, AI Engineering from 1 to 2, and Cloud stayed at 0. Explanations were longer in all three after-guide runs; length alone does not establish quality.

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
