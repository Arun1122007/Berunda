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
    data: {
      items: [
        {
          id: 1001,
          name: "Ramesh alias 'Blinking Ramu'",
          alias: "Blinking Ramu",
          age: 34,
          gender: "Male",
          primary_mo: "Cyber Banking Fraud / Phishing",
          jurisdiction: "Bengaluru City",
          case_count: 12,
          risk_status: "Critical",
          last_active: "2026-07-25",
        },
        {
          id: 1002,
          name: "Suresh Kumar",
          alias: "Suri",
          age: 29,
          gender: "Male",
          primary_mo: "Night House Break-in & Burglary",
          jurisdiction: "Mysuru District",
          case_count: 5,
          risk_status: "High",
          last_active: "2026-07-18",
        },
      ],
      total: 2,
    },
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
    expect(screen.getByText("Cyber Banking Fraud / Phishing")).toBeTruthy();
  });
});
