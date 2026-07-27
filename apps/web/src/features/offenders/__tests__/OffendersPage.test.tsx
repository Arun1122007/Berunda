import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import OffendersPage from "../pages/OffendersPage";

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
    data: [
      {
        personEntityId: 1001,
        canonicalName: "Ramesh alias 'Blinking Ramu'",
        gender: "Male",
        dob: "1992-03-15",
        primaryDistrictId: 1,
        updatedAt: "2026-07-25",
        createdAt: "2026-01-10",
      },
      {
        personEntityId: 1002,
        canonicalName: "Suresh Kumar",
        gender: "Male",
        dob: "1997-07-22",
        primaryDistrictId: 2,
        updatedAt: "2026-07-18",
        createdAt: "2026-02-05",
      },
    ],
    isLoading: false,
    error: null,
    refetch: vi.fn(),
  }),
}));

describe("OffendersPage", () => {
  it("renders the offender registry header and stats", () => {
    render(
      <BrowserRouter>
        <OffendersPage />
      </BrowserRouter>
    );

    expect(screen.getByText("Repeat & Flagged Offender Registry")).toBeTruthy();
    expect(screen.getByText(/Statewide database of habitual offenders/i)).toBeTruthy();
  });

  it("renders the offenders list in the table", () => {
    render(
      <BrowserRouter>
        <OffendersPage />
      </BrowserRouter>
    );

    expect(screen.getByText("Ramesh alias 'Blinking Ramu'")).toBeTruthy();
    expect(screen.getByText("Suresh Kumar")).toBeTruthy();
    expect(screen.getByText(/OFF-1001/)).toBeTruthy();
    expect(screen.getByText(/OFF-1002/)).toBeTruthy();
  });
});
