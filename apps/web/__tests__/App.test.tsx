/// <reference types="vitest" />
import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import App from "@/app/App";

test("renders the app without crashing", () => {
  expect(() =>
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
  ).not.toThrow();
});
