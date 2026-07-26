import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import InvestigationNotes from "../pages/InvestigationNotes";

vi.mock("@/hooks/useApi", () => ({
  useQuery: () => ({
    data: [
      {
        noteId: 1,
        caseMasterId: 1,
        authorId: 2,
        noteType: "general",
        content: "Initial investigation note.",
        isAmendment: false,
        visibility: "station",
        createdAt: "2026-07-20T10:30:00Z",
      },
      {
        noteId: 2,
        caseMasterId: 1,
        authorId: 3,
        noteType: "witness_statement",
        content: "Witness statement recorded.",
        isAmendment: false,
        visibility: "supervisor",
        createdAt: "2026-07-21T14:00:00Z",
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

describe("InvestigationNotes", () => {
  it("renders the component title", () => {
    render(<InvestigationNotes caseMasterId={1} />);
    expect(screen.getByText("Investigation Notes")).toBeTruthy();
  });

  it("renders list of notes", () => {
    render(<InvestigationNotes caseMasterId={1} />);
    expect(screen.getByText("Initial investigation note.")).toBeTruthy();
    expect(screen.getByText("Witness statement recorded.")).toBeTruthy();
  });

  it("shows note type badges", () => {
    render(<InvestigationNotes caseMasterId={1} />);
    expect(screen.getByText("general")).toBeTruthy();
  });

  it("shows Add Note button", () => {
    render(<InvestigationNotes caseMasterId={1} />);
    expect(screen.getByText("Add Note")).toBeTruthy();
  });
});
