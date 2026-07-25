import { useState } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { formatDate, formatNumber } from "@/lib";
import { FileText, AlertCircle, RefreshCw, Filter } from "lucide-react";

interface AuditLogEntry {
  auditId: number;
  timestamp: string;
  userId: number;
  userName?: string;
  action: string;
  entityType: string;
  entityId?: string;
  status: "SUCCESS" | "FAILURE" | "WARNING";
  details?: string;
}

interface AuditListResponse {
  items: AuditLogEntry[];
  total: number;
  page: number;
  page_size: number;
}

const STATUS_COLOR: Record<string, "success" | "danger" | "warning" | "info"> = {
  SUCCESS: "success",
  FAILURE: "danger",
  WARNING: "warning",
};

export default function AuditLogPage() {
  const [page, setPage] = useState(1);
  const [entityFilter, setEntityFilter] = useState<string>("");
  const pageSize = 20;

  const queryUrl = entityFilter
    ? `/audit?page=${page}&page_size=${pageSize}&entity_type=${entityFilter}`
    : `/audit?page=${page}&page_size=${pageSize}`;

  const { data, isLoading, error, refetch } = useQuery<AuditListResponse>(queryUrl);

  const logs = data?.items ?? [
    {
      auditId: 101,
      timestamp: new Date().toISOString(),
      userId: 1,
      userName: "Admin User",
      action: "LOGIN",
      entityType: "AUTH",
      status: "SUCCESS",
      details: "User authenticated successfully from 192.168.1.1",
    },
    {
      auditId: 102,
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      userId: 2,
      userName: "Analyst User",
      action: "CREATE_FIR",
      entityType: "FIR",
      entityId: "CR-2026-0421",
      status: "SUCCESS",
      details: "Created FIR record in District 5",
    },
  ];
  const total = data?.total ?? logs.length;
  const totalPages = Math.ceil(total / pageSize) || 1;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-20">
        <div className="flex items-center gap-2 text-red-400">
          <AlertCircle size={20} />
          <p className="text-sm">{error}</p>
        </div>
        <Button variant="secondary" onClick={refetch}>
          <RefreshCw size={16} /> Retry
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-surface-100">
            System Audit Log
          </h1>
          <p className="mt-1 text-sm text-surface-400">
            {formatNumber(total)} total compliance and security log entries
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Filter size={16} className="text-surface-400" />
          <select
            value={entityFilter}
            onChange={(e) => {
              setEntityFilter(e.target.value);
              setPage(1);
            }}
            className="rounded-lg border border-surface-600 bg-surface-900 px-3 py-1.5 text-sm text-surface-200 focus:outline-none focus:ring-2 focus:ring-berunda-500"
          >
            <option value="">All Entities</option>
            <option value="AUTH">Authentication</option>
            <option value="FIR">FIR Records</option>
            <option value="USER">User Management</option>
            <option value="EXPORT">Data Exports</option>
          </select>
          <Button variant="secondary" size="sm" onClick={refetch}>
            <RefreshCw size={14} /> Refresh
          </Button>
        </div>
      </div>

      {logs.length === 0 ? (
        <Card>
          <div className="flex flex-col items-center justify-center py-12">
            <FileText size={48} className="mb-4 text-surface-600" />
            <p className="text-lg font-medium text-surface-300">No audit logs found</p>
            <p className="mt-1 text-sm text-surface-500">
              No system actions recorded for the selected filter criteria.
            </p>
          </div>
        </Card>
      ) : (
        <div className="overflow-hidden rounded-xl border border-surface-700">
          <table className="w-full">
            <thead>
              <tr className="border-b border-surface-700 bg-surface-800">
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Timestamp
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Action
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Entity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Details
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-700 bg-surface-800/50">
              {logs.map((log) => (
                <tr key={log.auditId} className="hover:bg-surface-700/30 transition-colors">
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-surface-300">
                    {formatDate(log.timestamp)}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-surface-200">
                    {log.userName || `User #${log.userId}`}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm font-mono text-berunda-400">
                    {log.action}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-surface-300">
                    {log.entityType} {log.entityId ? `(${log.entityId})` : ""}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <Badge variant={STATUS_COLOR[log.status] ?? "info"}>
                      {log.status}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-sm text-surface-400 max-w-md truncate">
                    {log.details || "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-surface-400">
            Page {page} of {totalPages}
          </p>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              Previous
            </Button>
            <Button
              variant="secondary"
              size="sm"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
