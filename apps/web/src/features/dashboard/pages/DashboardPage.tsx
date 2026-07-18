import { useState } from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { Case, AnomalyAlert, RiskScore } from "@/types/api";

export default function DashboardPage() {
  const { data: cases, isLoading: casesLoading } = useQuery<Case[]>(
    "/cases?limit=5"
  );
  const { data: alerts, isLoading: alertsLoading } = useQuery<AnomalyAlert[]>(
    "/anomalies/recent"
  );
  const [selectedAlert, setSelectedAlert] = useState<string | null>(null);

  if (casesLoading || alertsLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

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
          <p className="mt-1 text-3xl font-bold text-surface-100">--</p>
        </Card>
        <Card>
          <p className="text-sm text-surface-400">Active Alerts</p>
          <p className="mt-1 text-3xl font-bold text-yellow-400">
            {alerts?.length || 0}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-surface-400">High Risk Persons</p>
          <p className="mt-1 text-3xl font-bold text-red-400">--</p>
        </Card>
        <Card>
          <p className="text-sm text-surface-400">Hotspots Active</p>
          <p className="mt-1 text-3xl font-bold text-berunda-400">--</p>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card header={<h2 className="font-semibold text-surface-100">Recent Cases</h2>}>
          {(!cases || cases.length === 0) ? (
            <p className="py-8 text-center text-sm text-surface-500">No recent cases</p>
          ) : (
            <div className="divide-y divide-surface-700">
              {cases.map((c) => (
                <div key={c.caseId} className="flex items-center justify-between py-3">
                  <div>
                    <p className="text-sm font-medium text-surface-200">
                      {c.caseNumber}
                    </p>
                    <p className="text-xs text-surface-400">{c.district}</p>
                  </div>
                  <Badge variant="info">{c.status}</Badge>
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
                  key={a.alertId}
                  className="flex items-center justify-between py-3 cursor-pointer"
                  onClick={() =>
                    setSelectedAlert(
                      selectedAlert === a.alertId ? null : a.alertId
                    )
                  }
                >
                  <div>
                    <p className="text-sm font-medium text-surface-200">
                      {a.crimeType} — {a.district}
                    </p>
                    <p className="text-xs text-surface-400">
                      Z-score: {a.zScore.toFixed(2)}
                    </p>
                  </div>
                  <Badge
                    variant={
                      a.severity === "critical" || a.severity === "high"
                        ? "danger"
                        : "warning"
                    }
                  >
                    {a.severity}
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
