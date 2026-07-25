/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import CaseListPage from "../pages/CaseListPage";

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

vi.mock("@/hooks/useApi", () => ({
  useQuery: () => ({
    data: {
      items: [
        {
          caseMasterId: 1,
          crimeNo: "CR-2026-0001",
          caseNo: "FIR/CR-2026-0001",
          crimeRegisteredDate: "2026-01-15T00:00:00",
          policeStationId: 5,
          caseStatusId: 1,
          crimeMajorHeadId: 1,
        },
        {
          caseMasterId: 2,
          crimeNo: "CR-2026-0002",
          caseNo: null,
          crimeRegisteredDate: "2026-02-20T00:00:00",
          policeStationId: 5,
          caseStatusId: 2,
          crimeMajorHeadId: 14,
        },
      ],
      total: 2,
      page: 1,
      page_size: 20,
    },
    isLoading: false,
    error: null,
    refetch: vi.fn(),
  }),
}));

describe("CaseListPage", () => {
  it("renders the case list with items", () => {
    render(
      <BrowserRouter>
        <CaseListPage />
      </BrowserRouter>
    );
    expect(screen.getByText("FIR Cases")).toBeTruthy();
    expect(screen.getByText("CR-2026-0001")).toBeTruthy();
    expect(screen.getByText("CR-2026-0002")).toBeTruthy();
  });

  it("shows total case count", () => {
    render(
      <BrowserRouter>
        <CaseListPage />
      </BrowserRouter>
    );
    expect(screen.getByText(/2 total cases/)).toBeTruthy();
  });

  it("shows New Case button for admin", () => {
    render(
      <BrowserRouter>
        <CaseListPage />
      </BrowserRouter>
    );
    expect(screen.getByText("New Case")).toBeTruthy();
  });
});
