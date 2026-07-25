import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { AuditEntry } from "@/types/api";
import { Users, Database, RefreshCw, Shield, ArrowRight, CheckCircle, Clock } from "lucide-react";
import clsx from "clsx";

type AdminTab = "overview" | "users" | "sources" | "jobs";

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<AdminTab>("overview");
  const navigate = useNavigate();

  const { data: auditLogs, isLoading } = useQuery<AuditEntry[]>(
    "/audit?page_size=10"
  );

  const mockUsers = [
    { id: 1, name: "Admin User", email: "admin@berunda.gov", role: "admin", status: "Active", district: "All (State HQ)" },
    { id: 2, name: "Analyst User", email: "analyst@berunda.gov", role: "analyst", status: "Active", district: "All (SCRB HQ)" },
    { id: 3, name: "Officer Sharma", email: "sharma@berunda.gov", role: "officer", status: "Active", district: "District 5" },
    { id: 4, name: "Officer Verma", email: "verma@berunda.gov", role: "officer", status: "Active", district: "District 12" },
  ];

  const mockSources = [
    { id: "SRC-01", name: "CCTNS Nightly Sync", type: "REST API", lastSync: "2026-07-25 04:00 IST", status: "Healthy", records: "2,410,291" },
    { id: "SRC-02", name: "Court Case Status Portal", type: "SOAP / XML", lastSync: "2026-07-25 05:30 IST", status: "Healthy", records: "841,020" },
    { id: "SRC-03", name: "Prisoner Release Records", type: "CSV Ingestion", lastSync: "2026-07-24 23:15 IST", status: "Warning", records: "112,490" },
  ];

  const mockJobs = [
    { id: "JOB-101", name: "Entity Resolution Graph Build", schedule: "0 2 * * * (Daily 2 AM)", nextRun: "In 3 hours", status: "Active", lastResult: "SUCCESS (14m 22s)" },
    { id: "JOB-102", name: "Hotspot Spatial Aggregation", schedule: "0 */4 * * * (Every 4h)", nextRun: "In 45 mins", status: "Active", lastResult: "SUCCESS (2m 10s)" },
    { id: "JOB-103", name: "Audit Log Archival & S3 Dump", schedule: "0 0 * * 0 (Weekly)", nextRun: "In 2 days", status: "Active", lastResult: "SUCCESS (5m 01s)" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-surface-100">Admin Console</h1>
          <p className="mt-1 text-sm text-surface-400">
            System configuration, data pipelines, and user access management
          </p>
        </div>

        <div className="flex rounded-lg bg-surface-800 p-1 border border-surface-700">
          {(["overview", "users", "sources", "jobs"] as AdminTab[]).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={clsx(
                "px-3 py-1.5 text-xs font-medium rounded-md transition-colors capitalize",
                activeTab === tab
                  ? "bg-berunda-600 text-white"
                  : "text-surface-400 hover:text-surface-200"
              )}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {activeTab === "overview" && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <Card className="cursor-pointer hover:border-surface-600 transition-colors" onClick={() => setActiveTab("users")}>
              <div className="flex items-center gap-3">
                <Users className="h-8 w-8 text-berunda-400" />
                <div>
                  <h3 className="font-medium text-surface-200">User Management</h3>
                  <p className="text-xs text-surface-400">Manage 4 analysts & officers &rarr;</p>
                </div>
              </div>
            </Card>

            <Card className="cursor-pointer hover:border-surface-600 transition-colors" onClick={() => setActiveTab("sources")}>
              <div className="flex items-center gap-3">
                <Database className="h-8 w-8 text-berunda-400" />
                <div>
                  <h3 className="font-medium text-surface-200">Data Sources</h3>
                  <p className="text-xs text-surface-400">3 active ingestion pipelines &rarr;</p>
                </div>
              </div>
            </Card>

            <Card className="cursor-pointer hover:border-surface-600 transition-colors" onClick={() => setActiveTab("jobs")}>
              <div className="flex items-center gap-3">
                <RefreshCw className="h-8 w-8 text-berunda-400" />
                <div>
                  <h3 className="font-medium text-surface-200">Scheduled Jobs</h3>
                  <p className="text-xs text-surface-400">3 cron jobs running &rarr;</p>
                </div>
              </div>
            </Card>
          </div>

          <Card
            header={
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Shield size={18} className="text-berunda-400" />
                  <h2 className="font-semibold text-surface-100">Recent Audit Logs</h2>
                </div>
                <Button variant="ghost" size="sm" onClick={() => navigate("/audit")} className="text-xs text-berunda-400">
                  View Full Audit Log <ArrowRight size={14} className="ml-1" />
                </Button>
              </div>
            }
          >
            {isLoading ? (
              <div className="py-8 flex justify-center"><LoadingSpinner /></div>
            ) : !auditLogs || auditLogs.length === 0 ? (
              <p className="py-8 text-center text-sm text-surface-500">No audit entries found</p>
            ) : (
              <div className="divide-y divide-surface-700">
                {auditLogs.map((log) => (
                  <div key={log.auditLogId} className="flex items-center justify-between py-3">
                    <div>
                      <p className="text-sm font-medium text-surface-200">
                        {log.action} — {log.entityType}
                      </p>
                      <p className="text-xs text-surface-400">
                        User #{log.userId} · {log.timestamp ? new Date(log.timestamp).toLocaleString() : "—"}
                      </p>
                    </div>
                    <Badge variant="info">{log.entityId || "SYSTEM"}</Badge>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </>
      )}

      {activeTab === "users" && (
        <Card header={<h2 className="font-semibold text-surface-100">Authorized Personnel Directory</h2>}>
          <div className="overflow-hidden rounded-lg border border-surface-700">
            <table className="w-full">
              <thead>
                <tr className="border-b border-surface-700 bg-surface-800 text-left text-xs uppercase text-surface-400">
                  <th className="px-4 py-3">Name</th>
                  <th className="px-4 py-3">Email</th>
                  <th className="px-4 py-3">Role</th>
                  <th className="px-4 py-3">Jurisdiction</th>
                  <th className="px-4 py-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-700 text-sm">
                {mockUsers.map((u) => (
                  <tr key={u.id} className="hover:bg-surface-700/30">
                    <td className="px-4 py-3 font-medium text-surface-200">{u.name}</td>
                    <td className="px-4 py-3 text-surface-400">{u.email}</td>
                    <td className="px-4 py-3"><Badge variant="info" className="uppercase">{u.role}</Badge></td>
                    <td className="px-4 py-3 text-surface-300">{u.district}</td>
                    <td className="px-4 py-3"><Badge variant="success">{u.status}</Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {activeTab === "sources" && (
        <Card header={<h2 className="font-semibold text-surface-100">Data Pipeline & Ingestion Status</h2>}>
          <div className="space-y-4">
            {mockSources.map((s) => (
              <div key={s.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-lg bg-surface-700/30 border border-surface-700 gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-berunda-400">{s.id}</span>
                    <h4 className="font-medium text-surface-200">{s.name}</h4>
                  </div>
                  <p className="text-xs text-surface-400 mt-1">
                    Protocol: {s.type} · Total Records: {s.records}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right text-xs text-surface-400">
                    <p>Last Sync</p>
                    <p className="text-surface-300 font-medium">{s.lastSync}</p>
                  </div>
                  <Badge variant={s.status === "Healthy" ? "success" : "warning"}>
                    {s.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {activeTab === "jobs" && (
        <Card header={<h2 className="font-semibold text-surface-100">Scheduled Cron & Maintenance Jobs</h2>}>
          <div className="space-y-4">
            {mockJobs.map((j) => (
              <div key={j.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-lg bg-surface-700/30 border border-surface-700 gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-berunda-400">{j.id}</span>
                    <h4 className="font-medium text-surface-200">{j.name}</h4>
                  </div>
                  <p className="text-xs text-surface-400 mt-1 flex items-center gap-1">
                    <Clock size={12} /> Schedule: {j.schedule} · Next run: {j.nextRun}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right text-xs">
                    <p className="text-surface-400">Last Execution</p>
                    <p className="text-green-400 flex items-center gap-1 justify-end font-medium">
                      <CheckCircle size={12} /> {j.lastResult}
                    </p>
                  </div>
                  <Badge variant="success">{j.status}</Badge>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
