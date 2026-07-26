import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import EvidenceManager from "../pages/EvidenceManager";

vi.mock("@/hooks/useApi", () => ({
  useQuery: () => ({
    data: [
      {
        evidenceId: 1,
        caseMasterId: 1,
        evidenceType: "photograph",
        description: "Crime scene photo",
        storagePath: "/evidence/photo1.jpg",
        collectedAt: "2026-01-16T10:00:00",
        collectedBy: "IO Sharma",
        source: "IO collection",
        location: "Main entrance",
        checksum: "abc123",
        fileType: "image/jpeg",
        fileSize: 2048576,
        status: "available",
        sensitivity: "sensitive",
        createdAt: "2026-01-16T10:00:00",
        updatedAt: "2026-01-16T10:00:00",
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

describe("EvidenceManager", () => {
  it("renders evidence list", () => {
    render(<EvidenceManager caseMasterId={1} />);
    expect(screen.getByText("Evidence")).toBeTruthy();
    expect(screen.getByText("Crime scene photo")).toBeTruthy();
    expect(screen.getByText("available")).toBeTruthy();
    expect(screen.getByText("sensitive")).toBeTruthy();
  });

  it("shows add evidence button", () => {
    render(<EvidenceManager caseMasterId={1} />);
    expect(screen.getByText("Add Evidence")).toBeTruthy();
  });
});
