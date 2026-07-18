# RAG Knowledge Base and Grounding Specification

[//]: # (Document ID: BERUNDA-AI-004 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Data Scientists | Source: 01_Enterprise_Blueprint §8 | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Overview

The "Ask Berunda" feature provides natural-language access to case information using Retrieval-Augmented Generation (RAG). The system retrieves relevant case facts from the knowledge base and generates grounded answers with citations.

## 2. Knowledge Base Construction

### 2.1 Source Documents

| Source | Content | Format | Chunking Strategy |
|--------|---------|--------|-------------------|
| src_CaseMaster.BriefFacts | FIR narrative | Text (NVARCHAR(MAX)) | Sentence-level, max 512 tokens with 50-token overlap |
| src_Act + src_Section | Legal act/section descriptions | Text | Per act-section (small, no chunking needed) |
| src_CrimeHead + src_CrimeSubHead | Crime classification hierarchy | Text | Per definition (small, no chunking needed) |

### 2.2 Chunking Pipeline

```
BriefFacts
  → Sentence splitting (spaCy sentencizer)
  → Token counting
  → Merge sentences until 512 tokens or natural break
  → 50-token overlap between chunks
  → Assign CaseMasterID + ChunkIndex
  → Store in int_RAGCorpusChunk
```

### 2.3 Embedding

| Parameter | Value |
|-----------|-------|
| Embedding model | QuickML LLM embedding endpoint |
| Vector dimension | 768 (QuickML default) |
| Storage | int_RAGCorpusChunk.Embedding column + Catalyst Cache for hot vectors |

## 3. Retrieval Pipeline

```
User Question
  → Embed question (QuickML LLM embedding)
  → Vector similarity search (cosine similarity) over int_RAGCorpusChunk
  → Top-K retrieval (K=5)
  → Role-aware filtering (remove chunks from restricted jurisdictions)
  → Re-rank by relevance score
  → Top-3 chunks → LLM prompt
```

## 4. Prompt Template

```
You are an investigative assistant for the Karnataka Police Department.
Answer the question based ONLY on the provided context.

Context:
[chunk_1_text]
[chunk_2_text]
[chunk_3_text]

If the context does not contain enough information to answer, say:
"Insufficient evidence in the available case records."

Always cite the source case number (CaseNo or CrimeNo) when referring to specific cases.

Question: [user_question]
Answer:
```

## 5. Pre-Defined Demo Questions

These questions are pre-tested and guaranteed to produce correct, grounded answers:

| # | Question | Expected Answer Type | Retrieved Cases |
|---|----------|---------------------|----------------|
| 1 | "How many FIRs were registered in Bengaluru Urban this year?" | Aggregate count | All cases in Bengaluru Urban district |
| 2 | "Show me all cases where Ramesh Kumar is mentioned." | Person search | Cases linked via PersonEntity |
| 3 | "What crimes are most common in Mysuru district?" | Crime head breakdown | Group by CrimeHeadName |
| 4 | "Which cases involved vehicle number KA-01-AB-1234?" | Vehicle-linked cases | VehicleLink lookup |
| 5 | "Is there a connection between the accused in case FIR-2024-001 and case FIR-2024-042?" | Hidden link discovery | RelationshipEdge traversal |

## 6. Edge Case Handling

| Scenario | Behavior |
|----------|----------|
| No relevant chunks found (max similarity < 0.70) | "Insufficient evidence..." |
| User asks for PII or restricted fields | "I cannot access caste or religion information." |
| User asks about data outside their jurisdiction | Answer omits results from restricted districts |
| LLM generates unsupported claim | Post-processing step verifies each claim maps to a retrieved chunk |
| Multiple questions in one query | Only the first question is answered (use follow-up for additional) |
| Non-case question ("What is the capital of France?") | "I can only answer questions about case records." |
