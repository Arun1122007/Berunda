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
const CaseListPage = React.lazy(
  () => import("@/features/cases/pages/CaseListPage")
);
const CaseDetailPage = React.lazy(
  () => import("@/features/cases/pages/CaseDetailPage")
);
const CreateCasePage = React.lazy(
  () => import("@/features/cases/pages/CreateCasePage")
);
const EditCasePage = React.lazy(
  () => import("@/features/cases/pages/EditCasePage")
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
const EntityPage = React.lazy(
  () => import("@/features/entities/pages/EntityPage")
);
const AskBerundaPage = React.lazy(
  () => import("@/features/rag/pages/AskBerundaPage")
);
const AdminPage = React.lazy(
  () => import("@/features/admin/pages/AdminPage")
);
const AuditLogPage = React.lazy(
  () => import("@/features/audit/pages/AuditLogPage")
);
const AnomaliesPage = React.lazy(
  () => import("@/features/anomalies/pages/AnomaliesPage")
);
const RiskPage = React.lazy(
  () => import("@/features/risk/pages/RiskPage")
);
const SocioeconomicPage = React.lazy(
  () => import("@/features/socioeconomic/pages/SocioeconomicPage")
);
const ImportPage = React.lazy(
  () => import("@/features/ingestion/pages/ImportPage")
);
const ReportsPage = React.lazy(
  () => import("@/features/reports/pages/ReportsPage")
);
const OffendersPage = React.lazy(
  () => import("@/features/offenders/pages/OffendersPage")
);
const OffenderDetailPage = React.lazy(
  () => import("@/features/offenders/pages/OffenderDetailPage")
);
const NotFoundPage = React.lazy(
  () => import("@/components/shared/NotFoundPage")
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
            <Route path="cases" element={<CaseListPage />} />
            <Route path="cases/new" element={<CreateCasePage />} />
            <Route path="cases/:id/edit" element={<EditCasePage />} />
            <Route path="cases/:id" element={<CaseDetailPage />} />
            <Route path="offenders" element={<OffendersPage />} />
            <Route path="offenders/:id" element={<OffenderDetailPage />} />
            <Route path="hotspot" element={<HotspotMapPage />} />
            <Route path="graph" element={<LinkGraphPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="entities" element={<EntityPage />} />
            <Route path="ask-berunda" element={<AskBerundaPage />} />
            <Route path="anomalies" element={<AnomaliesPage />} />
            <Route path="risk" element={<RiskPage />} />
            <Route path="socioeconomic" element={<SocioeconomicPage />} />
            <Route path="import" element={<ImportPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="admin" element={<AdminPage />} />
            <Route path="audit" element={<AuditLogPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}
