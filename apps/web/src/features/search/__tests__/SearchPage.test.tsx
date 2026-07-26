import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import SearchPage from "../pages/SearchPage";

vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => ({
    user: { userId: 1, role: "admin", email: "admin@test.com", name: "Admin", permissions: [] },
    isAuthenticated: true,
    isLoading: false,
    error: null,
    login: vi.fn(),
    demoLogin: vi.fn(),
    logout: vi.fn(),
  }),
}));

vi.mock("@/services/api-client", () => ({
  apiClient: {
    post: vi.fn().mockResolvedValue({
      items: [
        {
          caseMasterId: 1,
          crimeNo: "CR-2026-0001",
          crimeRegisteredDate: "2026-01-15T00:00:00",
          policeStationId: 5,
          caseStatusId: 1,
          briefFacts: "Sample case facts for testing",
          confidence: 0.95,
          matchReason: "Keyword match on brief facts",
        },
      ],
      total: 1,
      page: 1,
      pageSize: 20,
      semanticUsed: false,
    }),
  },
}));

describe("SearchPage", () => {
  it("renders the search page with heading and search input", () => {
    render(
      <BrowserRouter>
        <SearchPage />
      </BrowserRouter>
    );
    expect(screen.getByText("Search")).toBeTruthy();
    expect(screen.getByPlaceholderText(/Search by case details/)).toBeTruthy();
    expect(screen.getByText("Semantic Search")).toBeTruthy();
  });

  it("shows advanced filters toggle", () => {
    render(
      <BrowserRouter>
        <SearchPage />
      </BrowserRouter>
    );
    expect(screen.getByText("Filters")).toBeTruthy();
  });

  it("shows initial empty state with search prompt", () => {
    render(
      <BrowserRouter>
        <SearchPage />
      </BrowserRouter>
    );
    expect(screen.getByText("Search across all case data")).toBeTruthy();
  });
});
