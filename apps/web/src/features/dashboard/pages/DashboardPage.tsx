import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Shield, AlertTriangle, Users, MapPin, TrendingUp, Activity, FileText, ClipboardCheck, UserCheck, type LucideIcon } from "lucide-react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { useAuth } from "@/hooks/useAuth";
import { formatDate, formatNumber, timeAgo } from "@/lib";
import type { CaseListResponse, AnomalyAlert, RiskScore, DashboardMetrics } from "@/types/api";

function LiveDot() {
  return (
    <span className="relative flex h-2.5 w-2.5">
      <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75" />
      <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-green-500" />
    </span>
  );
}

function StatCard({ icon: Icon, label, value, color, sub }: {
  icon: LucideIcon;
  label: string;
  value: string | number;
  color: string;
  sub?: string;
}) {
  return (
    <div className="group relative overflow-hidden rounded-xl border border-surface-700 bg-surface-800 p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-berunda-700/50 hover:shadow-lg hover:shadow-berunda-900/10">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium tracking-wide text-surface-400 uppercase">{label}</p>
          <p className={`mt-1.5 text-3xl font-bold tracking-tight ${color}`}>
            {value}
          </p>
          {sub && (
            <p className="mt-0.5 text-xs text-surface-500">{sub}</p>
          )}
        </div>
        <div className="rounded-lg bg-surface-700/50 p-2.5 transition-colors group-hover:bg-berunda-600/10">
          <Icon size={20} className={`${color} transition-transform duration-200 group-hover:scale-110`} />
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { data: firList, isLoading: casesLoading } = useQuery<CaseListResponse>(
    "/fir?page_size=5"
  );
  const { data: alerts, isLoading: alertsLoading } = useQuery<AnomalyAlert[]>(
    "/anomalies?alert_only=true"
  );
  const { data: riskScores } = useQuery<RiskScore[]>(
    "/risk?min_score=0.7&page_size=1"
  );
  const { data: officerMetrics, isLoading: metricsLoading } = useQuery<DashboardMetrics>(
    "/dashboard/officer"
  );
  const { data: activity } = useQuery<{caseMasterId: number; crimeNo?: string; activityType: string; description?: string; timestamp?: string}[]>(
    "/dashboard/activity"
  );
  const [selectedAlert, setSelectedAlert] = useState<number | null>(null);

  const cases = firList?.items ?? [];
  const alertCount = alerts?.length ?? 0;
  const highRiskCount = riskScores?.filter((r) => r.score > 0.7).length ?? 0;
  const hotspotCount = alerts?.filter((a) => (a.zScore ?? 0) > 2).length ?? 0;
  const isSupervisor = user?.role === "supervisor" || user?.role === "admin";

  if (casesLoading || alertsLoading || metricsLoading) {
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
      <div className="relative overflow-hidden rounded-2xl border border-surface-700 bg-gradient-to-br from-surface-800 via-surface-800 to-berunda-950/30 px-8 py-7">
        <div className="absolute right-0 top-0 h-64 w-64 translate-x-16 -translate-y-16 rounded-full bg-berunda-600/5 blur-3xl" />
        <div className="relative flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-berunda-600/20">
            <Shield className="h-7 w-7 text-berunda-400" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-3">
              <h1 className="font-sans text-2xl font-bold tracking-tight text-surface-100">
                Crime Intelligence Center
              </h1>
              <div className="flex items-center gap-1.5 rounded-full border border-surface-600 bg-surface-700/50 px-2.5 py-0.5">
                <LiveDot />
                <span className="text-[11px] font-medium tracking-wide text-green-400 uppercase">Live</span>
              </div>
            </div>
            <p className="mt-1 text-sm text-surface-400">
              Real-time crime intelligence overview and monitoring for Karnataka State Police
            </p>
          </div>
          <div className="hidden items-center gap-2 rounded-lg border border-surface-700 bg-surface-800/50 px-4 py-2.5 sm:flex">
            <Activity size={16} className="text-surface-400" />
            <div className="text-right text-xs">
              <p className="text-surface-400">Last Updated</p>
              <p className="font-medium text-surface-200">{timeAgo(new Date().toISOString())}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={TrendingUp}
          label="Total Cases"
          value={formatNumber(firList?.total ?? 0)}
          color="text-berunda-400"
          sub="All registered across districts"
        />
        <StatCard
          icon={AlertTriangle}
          label="Active Alerts"
          value={alertCount}
          color="text-yellow-400"
          sub="Anomalies requiring attention"
        />
        <StatCard
          icon={Users}
          label="High Risk Persons"
          value={highRiskCount}
          color="text-red-400"
          sub="Risk score &gt; 0.7"
        />
        <StatCard
          icon={MapPin}
          label="Hotspots Active"
          value={hotspotCount}
          color="text-berunda-400"
          sub="Z-score &gt; 2.0"
        />
      </div>

      {/* Phase 4: Officer / Supervisor Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={FileText}
          label="My Assigned Cases"
          value={formatNumber(officerMetrics?.assignedToMeCount ?? 0)}
          color="text-berunda-400"
          sub="Currently assigned to you"
        />
        <StatCard
          icon={ClipboardCheck}
          label="Pending Reviews"
          value={formatNumber(officerMetrics?.pendingReviewCount ?? 0)}
          color="text-yellow-400"
          sub="Awaiting supervisor review"
        />
        <StatCard
          icon={UserCheck}
          label="Unassigned Cases"
          value={formatNumber(officerMetrics?.unassignedCount ?? 0)}
          color="text-orange-400"
          sub="Not yet assigned to any IO"
        />
        <StatCard
          icon={TrendingUp}
          label="Total in Station"
          value={formatNumber(officerMetrics?.totalFirs ?? 0)}
          color="text-berunda-400"
          sub="All cases in your jurisdiction"
        />
      </div>

      <div className="flex gap-4">
        <Button onClick={() => navigate("/cases/new")}>
          <FileText size={16} /> New FIR
        </Button>
        <Button variant="secondary" onClick={() => navigate("/cases")}>
          <ClipboardCheck size={16} /> View All Cases
        </Button>
        {isSupervisor && (
          <Button variant="secondary" onClick={() => navigate("/cases")}>
            <UserCheck size={16} /> Supervisor Review
          </Button>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card header={<h2 className="font-semibold text-surface-100">Recent Cases</h2>}>
          {cases.length === 0 ? (
            <p className="py-8 text-center text-sm text-surface-500">No recent cases</p>
          ) : (
            <div className="divide-y divide-surface-700">
              {cases.map((c) => (
                <div
                  key={c.caseMasterId}
                  className="flex items-center justify-between py-3 transition-colors hover:bg-surface-700/30 -mx-6 px-6 cursor-pointer"
                  onClick={() => navigate(`/cases/${c.caseMasterId}`)}
                >
                  <div>
                    <p className="text-sm font-medium text-surface-200">
                      {c.crimeNo}
                    </p>
                    <p className="text-xs text-surface-400">{c.caseNo || "—"}</p>
                  </div>
                  <Badge variant="info">{c.caseStatusId ? `Status ${c.caseStatusId}` : "Active"}</Badge>
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
                  className="flex items-center justify-between py-3 transition-colors hover:bg-surface-700/30 cursor-pointer -mx-6 px-6"
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

      <Card header={<h2 className="font-semibold text-surface-100">Recent Activity</h2>}>
        {(!activity || activity.length === 0) ? (
          <p className="py-8 text-center text-sm text-surface-500">No recent activity</p>
        ) : (
          <div className="divide-y divide-surface-700">
            {activity.map((a, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between py-3 transition-colors hover:bg-surface-700/30 -mx-6 px-6 cursor-pointer"
                onClick={() => navigate(`/cases/${a.caseMasterId}`)}
              >
                <div>
                  <p className="text-sm font-medium text-surface-200">
                    {a.crimeNo || `Case #${a.caseMasterId}`}
                  </p>
                  <p className="text-xs text-surface-400">{a.description || a.activityType}</p>
                </div>
                <span className="text-xs text-surface-500">
                  {a.timestamp ? formatDate(a.timestamp) : ""}
                </span>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
