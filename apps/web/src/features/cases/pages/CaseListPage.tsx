import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { useAuth } from "@/hooks/useAuth";
import { formatDate, formatNumber } from "@/lib";
import { Plus, FileText, AlertCircle, RefreshCw, Pencil, Trash2 } from "lucide-react";
import type { Case, CaseListResponse } from "@/types/api";

const STATUS_LABEL: Record<number, string> = {
  1: "Under Investigation",
  2: "Charge Sheeted",
  3: "Pending Trial",
  4: "Convicted",
  5: "Acquitted",
};

const STATUS_COLOR: Record<number, "info" | "warning" | "success" | "danger"> = {
  1: "warning",
  2: "info",
  3: "warning",
  4: "success",
  5: "info",
};

export default function CaseListPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [page, setPage] = useState(1);
  const pageSize = 20;

  const { data, isLoading, error, refetch } = useQuery<CaseListResponse>(
    `/fir?page=${page}&page_size=${pageSize}`
  );

  const cases = data?.items ?? [];
  const total = data?.total ?? 0;
  const totalPages = Math.ceil(total / pageSize);
  const canCreate = user?.role === "admin" || user?.role === "analyst";
  const canEdit = user?.role === "admin" || user?.role === "officer";
  const canDelete = user?.role === "admin";

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
            FIR Cases
          </h1>
          <p className="mt-1 text-sm text-surface-400">
            {formatNumber(total)} total case{total !== 1 ? "s" : ""}
            {user?.role === "officer" && " in your district"}
          </p>
        </div>
        {canCreate && (
          <Button onClick={() => navigate("/cases/new")}>
            <Plus size={16} /> New Case
          </Button>
        )}
      </div>

      {cases.length === 0 ? (
        <Card>
          <div className="flex flex-col items-center justify-center py-12">
            <FileText size={48} className="mb-4 text-surface-600" />
            <p className="text-lg font-medium text-surface-300">No cases found</p>
            <p className="mt-1 text-sm text-surface-500">
              {canCreate ? "Create your first case to get started." : "No cases available in your district."}
            </p>
            {canCreate && (
              <Button className="mt-4" onClick={() => navigate("/cases/new")}>
                <Plus size={16} /> Create Case
              </Button>
            )}
          </div>
        </Card>
      ) : (
        <div className="overflow-hidden rounded-xl border border-surface-700">
          <table className="w-full">
            <thead>
              <tr className="border-b border-surface-700 bg-surface-800">
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Crime No
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-surface-400">
                  Case No
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-surface-400">
                  Details
                </th>
                {(canEdit || canDelete) && (
                  <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-surface-400">
                    Actions
                  </th>
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-700 bg-surface-800/50">
              {cases.map((c: Case) => (
                <tr
                  key={c.caseMasterId}
                  className="cursor-pointer transition-colors hover:bg-surface-700/30"
                  onClick={() => navigate(`/cases/${c.caseMasterId}`)}
                >
                  <td className="whitespace-nowrap px-6 py-4">
                    <span className="text-sm font-medium text-berunda-400">
                      {c.crimeNo || "—"}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-surface-300">
                    {formatDate(c.crimeRegisteredDate)}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <Badge variant={STATUS_COLOR[c.caseStatusId ?? 1] ?? "info"}>
                      {STATUS_LABEL[c.caseStatusId ?? 1] ?? "Unknown"}
                    </Badge>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-surface-300">
                    {c.caseNo || "—"}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-right">
                    <span className="text-sm text-berunda-400 hover:text-berunda-300">
                      View &rarr;
                    </span>
                  </td>
                  {(canEdit || canDelete) && (
                    <td className="whitespace-nowrap px-6 py-4 text-right">
                      <div className="flex justify-end gap-1">
                        {canEdit && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => { e.stopPropagation(); navigate(`/cases/${c.caseMasterId}/edit`); }}
                          >
                            <Pencil size={14} />
                          </Button>
                        )}
                        {canDelete && (
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-red-400 hover:text-red-300"
                            onClick={(e) => {
                              e.stopPropagation();
                              if (confirm("Delete this case? This cannot be undone.")) {
                                navigate(`/cases/${c.caseMasterId}`);
                              }
                            }}
                          >
                            <Trash2 size={14} />
                          </Button>
                        )}
                      </div>
                    </td>
                  )}
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
