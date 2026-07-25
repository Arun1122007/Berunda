import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "@/app/App";
import "@/styles/globals.css";

// Conditionally load Zoho Catalyst Web SDK only in production
if (import.meta.env.PROD || import.meta.env.VITE_CATALYST_ENABLED === "true") {
  const script1 = document.createElement("script");
  script1.src =
    "https://static.zohocdn.com/catalyst/sdk/js/4.6.2/catalystWebSDK.js";
  document.head.appendChild(script1);

  const script2 = document.createElement("script");
  script2.src = "/__catalyst/sdk/init.js";
  script2.defer = true;
  document.head.appendChild(script2);
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
