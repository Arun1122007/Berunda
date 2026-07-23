### Key Findings and Problem Context

The Karnataka State Police (KSP) currently manages crime data in fragmented, Excel-based silos and legacy Crime and Criminal Tracking Network & Systems (CCTNS) databases [1-3]. This creates a reactive policing environment that lacks cross-case relationship intelligence, making it difficult to link suspects, vehicles, and locations across different districts [4, 5]. Furthermore, the State Crime Records Bureau (SCRB) receives delayed fragments of information instead of a structured, live feed [4]. 

**Project Berunda (NAMMA KSP)** was developed for the KSP Datathon 2026 to resolve these issues by establishing a proactive, AI-driven crime intelligence hub [6-8]. While existing enterprise platforms like Palantir Gotham or IBM i2 offer link analysis, they are proprietary, expensive, and not natively bilingual [9-11]. Berunda is distinct because it is an **open-source, state-owned prototype built mandatorily on Zoho Catalyst, features native bilingual NLP (Kannada and English), and integrates bias-auditing as a foundational component** rather than an afterthought [7, 10, 12-14].

### Architectural Decisions

Project Berunda utilizes a serverless, cloud-native modular microservices architecture deployed entirely on Zoho Catalyst [7, 15, 16]. 

**Cloud Infrastructure:**
*   **Compute:** API endpoints and business logic run on Catalyst AppSail (PaaS) and serverless Functions [17-19].
*   **Storage Tiering:** Catalyst Data Store (SQL) handles structured, relational crime records; Catalyst NoSQL stores unstructured case diaries and free text; Catalyst Stratus provides S3-style object storage for evidence files; and Catalyst Cache handles frequently accessed lookups like jurisdiction boundaries [20-23].
*   **Automation:** Catalyst Cron triggers scheduled operations (like nightly predictive model updates), and Catalyst Signals coordinates asynchronous event-routing [17, 19].

**AI and Analytical Architecture:**
*   **Conversational Assistant & NLP:** The system uses Groq and Mistral for Large Language Model (LLM) inference, integrated alongside **Sarvam AI** for Kannada/English speech-to-text and text-to-speech processing [19, 24].
*   **Predictive Analytics:** Zoho Catalyst QuickML handles AutoML tabular training for repeat-offender risk scoring and hotspot modelling [17, 18, 25]. 
*   **Link Analysis (Graph Computing):** In Phase 1, the platform relies on in-application graph traversals using NetworkX over relational join tables [15, 26]. For Phase 3 enterprise scale, the architecture mandates migrating to a dedicated graph database like Neo4j [26, 27].

### Datasets and Data Modeling

**Core Database Schema & Entity Resolution:**
The system is modeled on the real, confidential KSP FIR Entity-Relationship diagram, which includes core tables such as `CaseMaster`, `Inv_OccuranceTime`, `ComplainantDetails`, `Victim`, and `Accused` [28-30]. 
*   **Architectural Discovery:** The team identified that the official KSP schema scopes Accused and Victim records *per-case* with no linking identifier for individuals across multiple FIRs [31, 32]. To solve this, Berunda implements a **`PersonEntity` deduplication layer**, using phonetic name matching and address overlap to resolve and connect identities across jurisdictions [33, 34].

**Synthetic and Enrichment Data:**
Due to strict data privacy constraints, the hackathon prototype operates entirely on synthetic data [35, 36].
*   **Faker and Indic-faker** libraries are used to generate thousands of realistic FIRs and suspect profiles in both English and Kannada, deliberately planting repeat offenders and hotspot patterns to validate the system [37-39].
*   **Geospatial & Environmental Context:** Data is enriched using OpenStreetMap (for POIs like hospitals and ATMs), Bhuvan (for terrain layers), and IMD/Open-Meteo (for historical weather records) [37, 40-42].

**Ethical Governance and Exclusions:**
The official KSP schema legally requires recording `CasteID` and `ReligionID` for statutory reporting under the SC/ST Act [43, 44]. However, **Berunda architects hard-excluded these fields from all predictive models and risk scoring** to prevent discriminatory profiling [45, 46]. A "Governance & Bias-Audit Agent" programmatically ensures these attributes never influence model feature-importance [45, 46].

### Technical Gaps and Required Enterprise Hardening

The prototype demonstrates immense capability but possesses several severe constraints that must be remediated for a true production rollout:
*   **Authentication Vulnerability:** The prototype currently uses a `DEMO_MODE=true` flag that completely bypasses authentication. This must be replaced with Catalyst Native Authentication integrated with role-based access control (RBAC) [47-49].
*   **Volatile Storage:** Generated PDF intelligence reports are saved to ephemeral local containers. These must be migrated to Catalyst Stratus via the Python SDK for persistent, secure storage [50-52].
*   **API Security & Data Leakage:** The use of external cloud LLMs (Groq, Mistral, Sarvam) introduces risk. The roadmap mandates moving text parsing and NLP tasks to self-hosted enterprise models or native Catalyst Zia Services to guarantee data never leaves the secure KSP Wide Area Network (KSPWAN) [51-53].
*   **CCTNS Synchronization:** The current system uses static SQLite and flat files. The platform must migrate entirely to the Catalyst Data Store and establish secure read-only API contracts for live synchronization with official CCTNS staging environments [50, 51, 54, 55].

### Strategic Plans and Implementation Roadmap

The execution strategy transitions Project Berunda from an 11-day hackathon sprint to a 10-year enterprise vision [56-58]:

*   **Phase 1 — MVP (11-Day Hackathon):** Focuses on loading the synthetic dataset, deploying the English Named Entity Recognition (NER) pipeline, deduplicating entities, establishing Zia AutoML risk scoring, and finalizing the investigator dashboard and conversational AI demo [56, 59, 60].
*   **Phase 2 — District Pilot (~3 Months):** Rollout to a single police district using real CCTNS data under a data-sharing MOU. Features include activating Kannada NLP via AI4Bharat, MO fingerprinting, and establishing the human AI governance review board [57, 61].
*   **Phase 3 — District Deployment:** Transitioning to full event-driven orchestration (Catalyst Signals/Circuits), migrating network analysis to Neo4j, implementing attribute-based access control (ABAC), and building a blockchain-anchored evidence chain of custody [57, 62].
*   **Phase 4 — State Deployment (~12 Months):** Ingestion of 30 years of historical crime data, activating the state-wide SCRB command view, and potentially launching Open-Source Intelligence (OSINT) monitoring strictly post-legal review [58, 63].
*   **Phase 5 & 6 — National and International Rollout:** Expanding to cross-state crime correlations dependent on inter-state data-sharing MOUs, deep integration with the Inter-Operable Criminal Justice System (ICJS), and creating a federated National Crime Knowledge Graph [58, 64, 65].