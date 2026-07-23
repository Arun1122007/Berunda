import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { AuditEntry } from "@/types/api";
import { Settings, Users, Database, RefreshCw, Shield } from "lucide-react";

export default function AdminPage() {
  const { data: auditLogs, isLoading } = useQuery<AuditEntry[]>(
    "/audit?page_size=10"
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Admin</h1>
        <p className="mt-1 text-sm text-surface-400">
          System configuration and user management
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <div className="flex items-center gap-3">
            <Users className="h-8 w-8 text-berunda-400" />
            <div>
              <h3 className="font-medium text-surface-200">User Management</h3>
              <p className="text-xs text-surface-400">Manage analysts and roles</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-3">
            <Database className="h-8 w-8 text-berunda-400" />
            <div>
              <h3 className="font-medium text-surface-200">Data Sources</h3>
              <p className="text-xs text-surface-400">Configure import pipelines</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-3">
            <RefreshCw className="h-8 w-8 text-berunda-400" />
            <div>
              <h3 className="font-medium text-surface-200">Scheduled Jobs</h3>
              <p className="text-xs text-surface-400">Cron job management</p>
            </div>
          </div>
        </Card>
      </div>

      <Card
        header={
          <div className="flex items-center gap-2">
            <Shield size={18} className="text-berunda-400" />
            <h2 className="font-semibold text-surface-100">Recent Audit Logs</h2>
          </div>
        }
      >
        {isLoading ? (
          <LoadingSpinner />
        ) : !auditLogs || auditLogs.length === 0 ? (
          <p className="py-8 text-center text-sm text-surface-500">No audit entries</p>
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
                <Badge variant="info">{log.entityId}</Badge>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
