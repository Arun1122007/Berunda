import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import RelatedCasesPanel from "../pages/RelatedCasesPanel";

vi.mock("@/hooks/useApi", () => ({
  useQuery: () => ({
    data: [
      {
        suggestionId: 1,
        sourceFIRId: 1,
        candidateFIRId: 2,
        confidenceScore: 0.87,
        supportingSignals: "shared_vehicle,overlapping_witnesses",
        explanation: "Same vehicle number KA-01-XY-1234 linked to both cases",
        modelVersion: "v1.0",
        reviewStatus: "suggested",
        reviewedByUserId: null,
        reviewReason: null,
        reviewedAt: null,
        createdAt: "2026-07-15T12:00:00",
        candidateCrimeNo: "CR-2026-0042",
        candidateStatusId: 1,
      },
    ],
    isLoading: false,
    error: null,
    refetch: vi.fn(),
  }),
  useMutation: () => ({
    isLoading: false,
    error: null,
    mutate: vi.fn(),
    reset: vi.fn(),
  }),
}));

describe("RelatedCasesPanel", () => {
  it("renders related case suggestions", () => {
    render(
      <MemoryRouter>
        <RelatedCasesPanel caseMasterId={1} />
      </MemoryRouter>
    );
    expect(screen.getByText("Related Cases")).toBeTruthy();
    expect(screen.getByText("CR-2026-0042")).toBeTruthy();
    expect(screen.getByText("87%")).toBeTruthy();
    expect(screen.getByText(/Same vehicle number/)).toBeTruthy();
  });

  it("shows review button for suggested status", () => {
    render(
      <MemoryRouter>
        <RelatedCasesPanel caseMasterId={1} />
      </MemoryRouter>
    );
    expect(screen.getByText("Review Suggestion")).toBeTruthy();
  });
});
