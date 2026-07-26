import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import CaseDetailPage from "../pages/CaseDetailPage";

vi.mock("@/hooks/useApi", () => ({
  useQuery: (url: string) => {
    if (url && (url.includes("/notes") || url.includes("/related-cases") || url.includes("/evidence") || url.includes("/timeline"))) {
      return { data: [], isLoading: false, error: null, refetch: vi.fn() };
    }
    return {
      data: {
        caseMasterId: 1,
        crimeNo: "CR-2026-0001",
        caseNo: "42/2026",
        crimeRegisteredDate: "2026-01-15T00:00:00",
        policeStationId: 5,
        caseStatusId: 1,
        crimeMajorHeadId: 1,
        crimeMinorHeadId: 1,
        incidentFromDate: "2026-01-14T20:30:00",
        incidentToDate: "2026-01-14T23:45:00",
        latitude: 12.9716,
        longitude: 77.5946,
        briefFacts: "Test incident description with details.",
        complainants: [
          { complainantName: "John Doe", ageYear: 35 },
        ],
        victims: [
          { victimName: "Jane Doe", ageYear: 28 },
        ],
        accused: [
          { accusedName: "Suspect A", ageYear: 42 },
        ],
        actSections: [],
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    };
  },
  useMutation: () => ({
    isLoading: false,
    error: null,
    mutate: vi.fn(),
    reset: vi.fn(),
  }),
}));

describe("CaseDetailPage", () => {
  it("renders case details", () => {
    render(
      <MemoryRouter initialEntries={["/cases/1"]}>
        <Routes>
          <Route path="/cases/:id" element={<CaseDetailPage />} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByText("CR-2026-0001")).toBeTruthy();
    expect(screen.getByText("Test incident description with details.")).toBeTruthy();
  });

  it("shows related persons sections", () => {
    render(
      <MemoryRouter initialEntries={["/cases/1"]}>
        <Routes>
          <Route path="/cases/:id" element={<CaseDetailPage />} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByText(/Complainants/)).toBeTruthy();
    expect(screen.getByText(/Victims/)).toBeTruthy();
    expect(screen.getByText(/Accused/)).toBeTruthy();
  });

  it("shows location data", () => {
    render(
      <MemoryRouter initialEntries={["/cases/1"]}>
        <Routes>
          <Route path="/cases/:id" element={<CaseDetailPage />} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByText("12.971600")).toBeTruthy();
    expect(screen.getByText("77.594600")).toBeTruthy();
  });

  it("shows back button", () => {
    render(
      <MemoryRouter initialEntries={["/cases/1"]}>
        <Routes>
          <Route path="/cases/:id" element={<CaseDetailPage />} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByText("Back")).toBeTruthy();
  });
});
