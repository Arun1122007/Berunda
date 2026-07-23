import { useState } from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { CaseListResponse, AnomalyAlert, RiskScore } from "@/types/api";

export default function DashboardPage() {
  const { data: firList, isLoading: casesLoading } = useQuery<CaseListResponse>(
    "/fir?page_size=5"
  );
  const { data: alerts, isLoading: alertsLoading } = useQuery<AnomalyAlert[]>(
    "/anomalies?alert_only=true"
  );
  const { data: riskScores } = useQuery<RiskScore[]>(
    "/risk?min_score=0.7&page_size=1"
  );
  const [selectedAlert, setSelectedAlert] = useState<number | null>(null);

  const cases = firList?.items ?? [];

  if (casesLoading || alertsLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  const severity = (z: number | undefined): "danger" | "warning" | "info" => {
    if (!z) return "info";
    if (z > 3) return "danger";
    if (z > 2) return "warning";
    return "info";
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Dashboard</h1>
        <p className="mt-1 text-sm text-surface-400">
          Crime intelligence overview and monitoring
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <p className="text-sm text-surface-400">Total Cases</p>
          <p className="mt-1 text-3xl font-bold text-surface-100">{firList?.total ?? "--"}</p>
        </Card>
        <Card>
          <p className="text-sm text-surface-400">Active Alerts</p>
          <p className="mt-1 text-3xl font-bold text-yellow-400">
            {alerts?.length || 0}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-surface-400">High Risk Persons</p>
          <p className="mt-1 text-3xl font-bold text-red-400">
            {riskScores ? riskScores.filter((r) => r.score > 0.7).length : "--"}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-surface-400">Hotspots Active</p>
          <p className="mt-1 text-3xl font-bold text-berunda-400">
            {alerts?.filter((a) => (a.zScore ?? 0) > 2).length || "--"}
          </p>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card header={<h2 className="font-semibold text-surface-100">Recent Cases</h2>}>
          {cases.length === 0 ? (
            <p className="py-8 text-center text-sm text-surface-500">No recent cases</p>
          ) : (
            <div className="divide-y divide-surface-700">
              {cases.map((c) => (
                <div key={c.caseMasterId} className="flex items-center justify-between py-3">
                  <div>
                    <p className="text-sm font-medium text-surface-200">
                      {c.crimeNo}
                    </p>
                    <p className="text-xs text-surface-400">{c.caseNo || "—"}</p>
                  </div>
                  <Badge variant="info">{c.caseStatusId ? "Active" : "Closed"}</Badge>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card
          header={<h2 className="font-semibold text-surface-100">Anomaly Alerts</h2>}
        >
          {(!alerts || alerts.length === 0) ? (
            <p className="py-8 text-center text-sm text-surface-500">
              No active alerts
            </p>
          ) : (
            <div className="divide-y divide-surface-700">
              {alerts.map((a) => (
                <div
                  key={a.anomalyAlertId}
                  className="flex items-center justify-between py-3 cursor-pointer"
                  onClick={() =>
                    setSelectedAlert(
                      selectedAlert === a.anomalyAlertId ? null : a.anomalyAlertId
                    )
                  }
                >
                  <div>
                    <p className="text-sm font-medium text-surface-200">
                      District {a.districtId} — CrimeHead {a.crimeHeadId}
                    </p>
                    <p className="text-xs text-surface-400">
                      Z-score: {a.zScore?.toFixed(2) ?? "—"}
                    </p>
                  </div>
                  <Badge variant={severity(a.zScore)}>
                    {a.zScore && a.zScore > 2 ? "high" : "normal"}
                  </Badge>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
