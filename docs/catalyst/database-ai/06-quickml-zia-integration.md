# 06 - QuickML & Zia Integration

## Architecture
The application uses the Provider Abstraction Pattern.

```text
FastAPI Route
    ↓
AI Application Service (e.g. RAGService)
    ↓
AI Provider Interface
    ├── CatalystQuickMLAdapter
    ├── CatalystZiaAdapter
    └── LocalMockAdapter
```

## Catalyst QuickML
**Knowledge Base & RAG**:
- Instead of using custom FAISS/ChromaDB with OpenAI, we will use QuickML's document indexing.
- Documents uploaded to Stratus will be parsed and indexed into QuickML.
- Queries will be routed to QuickML for retrieval and generative synthesis.

**ZCQL Support**:
- For structured natural language querying of the FIR Database, QuickML will be used to translate NL -> Structured Intent (JSON) which we will manually validate and turn into safe ZCQL queries.

## Catalyst Zia
**OCR & Document Processing**:
- Zia OCR service will be invoked when legacy FIR PDFs are uploaded to Stratus.
- Extracted text will be cleaned and sent to QuickML.

**Text Analytics (NER)**:
- Instead of manual regex parsing, Zia Text Analytics will be used for Entity Extraction (Names, Locations, Dates) during the FIR ingestion pipeline to populate the `int_PersonEntity` table.

## Local Development
Since QuickML/Zia require valid Zoho Catalyst credentials and network connectivity, developers will use the `LocalMockAdapter` which returns deterministic JSON responses when `APP_ENV=local`.
