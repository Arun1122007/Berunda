import { useState } from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { Plus, AlertCircle, RefreshCw, User, History } from "lucide-react";
import type { CaseAssignment, CaseAssignmentCreate } from "@/types/api";

interface CaseAssignmentsProps {
  caseMasterId: number;
}

const ASSIGNMENT_STATUS_COLOR: Record<string, "info" | "warning" | "success" | "danger"> = {
  active: "success",
  completed: "info",
  reassigned: "warning",
  cancelled: "danger",
};

export default function CaseAssignments({ caseMasterId }: CaseAssignmentsProps) {
  const [showForm, setShowForm] = useState(false);
  const [officerId, setOfficerId] = useState("");
  const [reason, setReason] = useState("");

  const { data: assignments, isLoading, error, refetch } = useQuery<CaseAssignment[]>(
    `/fir/${caseMasterId}/assignments`
  );

  const { data: activeAssignment } = useQuery<CaseAssignment>(
    `/fir/${caseMasterId}/assignment/active`,
    { enabled: true }
  );

  const { isLoading: isCreating, mutate: createAssignment } = useMutation<CaseAssignment>(
    `/fir/${caseMasterId}/assignments`
  );

  const handleAssign = async () => {
    if (!officerId.trim()) return;
    const result = await createAssignment({
      assignedOfficerId: Number(officerId),
      assignmentReason: reason.trim() || undefined,
    } as CaseAssignmentCreate);
    if (result) {
      setOfficerId("");
      setReason("");
      setShowForm(false);
      refetch();
    }
  };

  if (error) {
    return (
      <Card header={<h3 className="font-semibold text-surface-100">Case Assignments</h3>}>
        <div className="flex flex-col items-center justify-center gap-3 py-8">
          <div className="flex items-center gap-2 text-red-400">
            <AlertCircle size={16} />
            <p className="text-sm">{error}</p>
          </div>
          <Button variant="secondary" size="sm" onClick={refetch}>
            <RefreshCw size={14} /> Retry
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card
      header={
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-surface-100">Case Assignments</h3>
          <Button variant="secondary" size="sm" onClick={() => setShowForm(!showForm)} disabled={isLoading}>
            <Plus size={14} /> Assign Officer
          </Button>
        </div>
      }
    >
      {showForm && (
        <div className="mb-4 space-y-3 rounded-lg bg-surface-700/30 p-4">
          <input
            type="number"
            value={officerId}
            onChange={(e) => setOfficerId(e.target.value)}
            placeholder="Officer User ID"
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200 placeholder-surface-500"
          />
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Assignment reason (optional)"
            rows={2}
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200 placeholder-surface-500"
          />
          <div className="flex gap-2">
            <Button size="sm" isLoading={isCreating} onClick={handleAssign}>
              Assign
            </Button>
            <Button variant="secondary" size="sm" onClick={() => setShowForm(false)}>
              Cancel
            </Button>
          </div>
        </div>
      )}

      {isLoading ? (
        <div className="flex justify-center py-8">
          <LoadingSpinner size="md" />
        </div>
      ) : !assignments || assignments.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-surface-500">
          <User size={32} className="mb-2" />
          <p className="text-sm">No assignments yet. Assign an officer to this case.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {activeAssignment && (
            <div className="rounded-lg border border-green-700/50 bg-green-900/10 p-3">
              <div className="flex items-center gap-2 mb-1">
                <Badge variant="success">Active</Badge>
                <span className="text-sm font-medium text-surface-200">
                  Officer #{activeAssignment.assignedOfficerId}
                </span>
                <span className="ml-auto text-xs text-surface-500">
                  {activeAssignment.assignedAt
                    ? new Date(activeAssignment.assignedAt).toLocaleDateString()
                    : ""}
                </span>
              </div>
              {activeAssignment.assignmentReason && (
                <p className="text-xs text-surface-400">{activeAssignment.assignmentReason}</p>
              )}
            </div>
          )}

          <div>
            <div className="mb-2 flex items-center gap-2 text-xs font-medium text-surface-400">
              <History size={14} /> Assignment History
            </div>
            <div className="space-y-2">
              {assignments.map((a) => (
                <div
                  key={a.assignmentId}
                  className="flex items-center justify-between rounded-lg border border-surface-700 bg-surface-800/30 p-3"
                >
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-surface-200">
                      Officer #{a.assignedOfficerId}
                    </p>
                    {a.assignmentReason && (
                      <p className="text-xs text-surface-400">{a.assignmentReason}</p>
                    )}
                    <p className="text-xs text-surface-500">
                      {a.assignedAt ? new Date(a.assignedAt).toLocaleString() : ""}
                      {a.endedAt ? ` — ${new Date(a.endedAt).toLocaleString()}` : ""}
                    </p>
                  </div>
                  <Badge variant={ASSIGNMENT_STATUS_COLOR[a.status || "active"] || "info"}>
                    {a.status || "active"}
                  </Badge>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}
