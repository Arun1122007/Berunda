import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import App from "@/app/App";

test("renders the app without crashing", () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
  const heading = screen.getByText(/Berunda/i);
  expect(heading).toBeInTheDocument();
});
