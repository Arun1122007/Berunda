# Project Berunda — Hackathon Submission & Pitch
## Companion document 2 of 5 — Karnataka State Police Datathon 2026

This is the judge-facing document — concise, demo-oriented, and explicit about what's live vs. what's roadmap. Use this as your presentation backbone; pull supporting depth from the full Enterprise Blueprint if a judge asks a follow-up question.

---

## 1. The Name

**Project Berunda** — named for the *Gandaberunda*, the two-headed mythical bird that is Karnataka's own state emblem (it's on every KSRTC bus in the state). The two heads are the design metaphor: one looks backward across historical case data to find hidden connections between cases; the other looks forward, forecasting where incidents are statistically likely, so patrols can be proactive instead of reactive. It's not a generic Sanskrit buzzword — it's specifically Karnataka's, and it's not used by any other tech product (checked).

## 2. The Problem, in Three Lines

Karnataka Police records live in station-level silos. A suspect involved in five incidents across three districts currently looks like five unrelated case files, because nothing cross-references people, vehicles, and locations across cases. SCRB gets fragments, not a live picture, and patrol deployment happens after crime spikes, not before.

## 3. What We Actually Found When We Read the Real Dataset

Most teams will build a dashboard on top of the provided schema and call it done. We read the ER diagram closely enough to find the thing that actually matters:

**The schema has no concept of "this is the same person across cases."** `Accused`/`Victim` records are scoped per-FIR — there's no field linking "Suresh, accused in Case #1" to "Suresh, accused in Case #5." The headline feature every team will pitch — "we connect suspects across cases!" — isn't something you get from the data as given. **We built the entity-resolution layer that makes it real** (`PersonEntity` — see live demo, step 2 below).

We also found `CasteID`/`ReligionID` fields on the complainant table. These exist for a legitimate reason — SC/ST Act and communal-crime statutory reporting, the same kind of data NCRB itself publishes to protect these communities. We didn't hide them and we didn't expose them naively — we hard-excluded them from every predictive model and access-restricted them to a dedicated compliance-reporting role. **We can show this working live** (see step 5).

## 4. Live Demo Script (Recommended Order)

1. **FIR intake** — a new synthetic FIR comes in, narrative text gets parsed, entities extracted.
2. **Entity resolution** — the accused person in this new FIR resolves to an existing `PersonEntity` with 3 prior cases across 2 districts, surfaced automatically. *(This is the moment that should land hardest — narrate explicitly that this doesn't come free from the schema, you built it.)*
3. **Risk score with visible reasoning** — click into that person, see a repeat-offender risk score with a feature-importance breakdown an officer can actually read.
4. **Hotspot map** — district → station drill-down, showing the manufactured hotspot week clearly flagged.
5. **Fairness check, live** — show the Governance & Bias-Audit output confirming caste/religion never appear in that risk score's features, and that the general dashboard role can't even query those columns. *(Say out loud: "we're not claiming ethical AI on a slide, here's the check running.")*
6. **"Ask Berunda"** — type a plain-English question ("summarize open cases linked to this vehicle"), get a grounded, cited answer.
7. **Close on the roadmap slide** (Section 8 below) — 30 seconds, no more.

## 5. What's Live vs. What's Roadmap (say this explicitly, don't let a judge catch you first)

| Live in the demo | Documented as roadmap, not built |
|---|---|
| English FIR NER + entity resolution | Kannada NLP (design complete, model swap pending) |
| Explainable risk scoring, bias-audited | OSINT/dark-web monitoring (legal review required first) |
| Hotspot mapping, anomaly detection | Cross-state correlation (needs data-sharing agreements) |
| Link-analysis graph traversal | Blockchain-anchored evidence chain (Phase 3 target) |
| "Ask Berunda" RAG Q&A | Voice intake, push notifications |

## 6. Why We're Different (not just "AI-powered")

Judges will see 5-10 teams with a dashboard, a heatmap, a prediction model, a network graph, and a chatbot. We have all five too — that's table stakes. What's rare:

1. We identified and solved the actual data-modeling gap in the real schema (entity resolution), not just the surface-level dashboard ask.
2. We designed around a real sensitive-data field (caste/religion) instead of ignoring it or exposing it — and can prove it live.
3. We're bilingual by design, not just "multi-language support" as a slide bullet.
4. We can name specific real systems (CCTNS, NCRB, Palantir Gotham, DataWalk, PredPol) and say precisely where we sit relative to each — not vague superiority claims.

## 7. Mandatory Catalyst Compliance (quick reference)

Every required capability from the Resources-tab table maps to a specific Catalyst service — full 26-row mapping with rationale is in the Enterprise Blueprint (Section 15). Headline ones judges will check first: Data Store (schema), QuickML (LLM/RAG + AutoML risk scoring — both native, not custom-built), Authentication + API Gateway (access control), Zia Services (OCR/entity extraction), Stratus (evidence storage).

## 8. The Roadmap Close (30-Second Version)

"This isn't a hackathon toy — Phase 1 is what you're watching right now. Phase 2 is a real district pilot with real CCTNS data. Phase 3-5 take this from one district to the whole state to the country. Full roadmap and risk analysis in our submitted documentation." *(Point to companion doc `Project_Berunda_Complete_Roadmap.md`.)*

## 9. Anticipated Judge Questions (prep these answers)

- **"How is this different from just using Palantir Gotham?"** → Cost, closed-source, not built for an Indian state police context, no native Kannada support, no built-in bias governance for this specific misuse pattern.
- **"Isn't predictive policing inherently biased?"** → Yes, that's a documented real risk (name PredPol's feedback-loop criticism specifically) — that's exactly why the fairness audit is a live, demoable part of the system, not a claim.
- **"Why does your schema have caste/religion fields at all?"** → Because Indian law requires it for SC/ST-Act protection purposes; explain the access-restriction architecture (Section 3 above), don't get defensive about the field's existence.
- **"What happens when you scale to 10M records?"** → Point to the Phase 3 graph-database migration and the storage-tiering strategy in the Blueprint (Section 6.5) — you have a specific answer, not a hand-wave.
