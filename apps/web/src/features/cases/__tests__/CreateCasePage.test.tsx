/// <reference types="vitest" />
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import CreateCasePage from "../pages/CreateCasePage";

vi.mock("@/hooks/useApi", () => ({
  useMutation: () => ({
    isLoading: false,
    error: null,
    mutate: vi.fn().mockResolvedValue({ caseMasterId: 99, crimeNo: "CR-2026-DEMO" }),
    reset: vi.fn(),
  }),
}));

describe("CreateCasePage", () => {
  it("renders the create case form", () => {
    render(
      <BrowserRouter>
        <CreateCasePage />
      </BrowserRouter>
    );
    expect(screen.getByText("Create New Case")).toBeTruthy();
    expect(screen.getByText("Crime No *")).toBeTruthy();
  });

  it("shows validation error when crimeNo is empty on submit", async () => {
    render(
      <BrowserRouter>
        <CreateCasePage />
      </BrowserRouter>
    );
    const submitBtn = screen.getByText("Create Case");
    fireEvent.click(submitBtn);
    expect(screen.getByText("Crime No is required")).toBeTruthy();
  });

  it("allows typing in crime number field", () => {
    render(
      <BrowserRouter>
        <CreateCasePage />
      </BrowserRouter>
    );
    const input = screen.getByLabelText("Crime No *") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "CR-2026-TEST" } });
    expect(input.value).toBe("CR-2026-TEST");
  });

  it("shows cancel button", () => {
    render(
      <BrowserRouter>
        <CreateCasePage />
      </BrowserRouter>
    );
    expect(screen.getByText("Cancel")).toBeTruthy();
  });
});
