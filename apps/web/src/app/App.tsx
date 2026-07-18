import React, { Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import ErrorBoundary from "@/components/ui/ErrorBoundary";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import Layout from "@/components/layout/Layout";
import ProtectedRoute from "@/components/shared/ProtectedRoute";
import "./App.css";

const DashboardPage = React.lazy(
  () => import("@/features/dashboard/pages/DashboardPage")
);
const HotspotMapPage = React.lazy(
  () => import("@/features/hotspot/pages/HotspotMapPage")
);
const LinkGraphPage = React.lazy(
  () => import("@/features/graph/pages/LinkGraphPage")
);
const AnalyticsPage = React.lazy(
  () => import("@/features/analytics/pages/AnalyticsPage")
);
const AskBerundaPage = React.lazy(
  () => import("@/features/rag/pages/AskBerundaPage")
);
const AdminPage = React.lazy(
  () => import("@/features/admin/pages/AdminPage")
);
const LoginPage = React.lazy(
  () => import("@/features/auth/pages/LoginPage")
);

export default function App() {
  return (
    <ErrorBoundary>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<DashboardPage />} />
            <Route path="hotspot" element={<HotspotMapPage />} />
            <Route path="graph" element={<LinkGraphPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="ask-berunda" element={<AskBerundaPage />} />
            <Route path="admin" element={<AdminPage />} />
          </Route>
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}
