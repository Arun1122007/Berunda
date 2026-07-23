const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { query, districtId, topK = 5 } = event?.data || {};

  if (!query) {
    return context.closeWithFailure({ error: "query is required" });
  }

  const table = ctx.datastore().table("int_RAGCorpusChunk");
  const filters = {};
  if (districtId) filters.DistrictID = districtId;

  const chunks = await table.getAllRows(filters);
  const queryLower = query.toLowerCase();

  const scored = chunks
    .map((c) => ({
      chunk: c,
      score: ((c.ChunkText || "").toLowerCase().includes(queryLower) ? 0.8 : 0.1) / (c.ChunkIndex || 1),
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);

  const citations = scored.map((s) => ({
    caseMasterId: s.chunk.CaseMasterID,
    text: (s.chunk.ChunkText || "").slice(0, 200),
    relevance: s.score,
  }));

  const answer = citations.length > 0
    ? `Found ${citations.length} relevant case chunks.`
    : "No relevant cases found for your query.";

  context.closeWithSuccess({ answer, citations, confidence: citations.length / topK });
};
