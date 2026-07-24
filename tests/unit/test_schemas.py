from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.schemas.auth import LoginRequest, UserResponse
from src.schemas.entity import EntityMergeRequest, EntitySearchQuery
from src.schemas.fir import FIRCreate, FIRResponse
from src.schemas.graph import GraphEdgeResponse, GraphNodeResponse, GraphQuery
from src.schemas.rag import RAGCitation, RAGQuery
from src.schemas.risk import RiskScoreQuery, RiskScoreResponse


class TestFIRSchemas:
    def test_fir_create_valid(self):
        data = FIRCreate(CrimeNo="1-2345-6789-0123-45678")
        assert data.CrimeNo == "1-2345-6789-0123-45678"

    def test_fir_create_minimal(self):
        data = FIRCreate(CrimeNo="TEST-001")
        assert data.CrimeNo == "TEST-001"
        assert data.CaseNo is None

    def test_fir_response_from_attributes(self):
        resp = FIRResponse(
            CaseMasterID=1,
            CrimeNo="1-2345-6789-0123-45678",
        )
        assert resp.CaseMasterID == 1
        assert resp.CrimeNo == "1-2345-6789-0123-45678"


class TestEntitySchemas:
    def test_entity_search_defaults(self):
        q = EntitySearchQuery()
        assert q.page == 1
        assert q.page_size == 20
        assert q.name is None

    def test_entity_search_custom(self):
        q = EntitySearchQuery(name="test", district_id=5, page=2, page_size=10)
        assert q.name == "test"
        assert q.district_id == 5
        assert q.page == 2
        assert q.page_size == 10

    def test_entity_merge_request(self):
        req = EntityMergeRequest(source_entity_id=1, target_entity_id=2)
        assert req.source_entity_id == 1
        assert req.target_entity_id == 2


class TestGraphSchemas:
    def test_graph_query_defaults(self):
        q = GraphQuery()
        assert q.max_depth == 2
        assert q.min_confidence == 0.5

    def test_graph_node(self):
        n = GraphNodeResponse(id="1", label="Test", type="person")
        assert n.id == "1"
        assert n.label == "Test"
        assert n.type == "person"

    def test_graph_edge(self):
        e = GraphEdgeResponse(source="1", target="2", label="co-accused", weight=0.85)
        assert e.source == "1"
        assert e.target == "2"
        assert e.weight == 0.85


class TestRAGSchemas:
    def test_rag_query_min_query(self):
        with pytest.raises(ValidationError):
            RAGQuery(query="")

    def test_rag_query_valid(self):
        q = RAGQuery(query="test query", top_k=3)
        assert q.query == "test query"
        assert q.top_k == 3

    def test_rag_citation(self):
        c = RAGCitation(CaseMasterID=1, ChunkText="test", Relevance=0.9)
        assert c.CaseMasterID == 1
        assert c.Relevance == 0.9


class TestAuthSchemas:
    def test_login_request(self):
        req = LoginRequest(email="admin@test.com", password="pass")
        assert req.email == "admin@test.com"
        assert req.password == "pass"

    def test_user_response(self):
        u = UserResponse(userId=1, email="admin@test.com", name="Admin", role="admin")
        assert u.userId == 1
        assert u.role == "admin"
        assert u.permissions == []


class TestRiskSchemas:
    def test_risk_query_defaults(self):
        q = RiskScoreQuery()
        assert q.page == 1
        assert q.page_size == 20

    def test_risk_response(self):
        r = RiskScoreResponse(RiskScoreID=1, PersonEntityID=1, Score=0.75)
        assert r.Score == 0.75
