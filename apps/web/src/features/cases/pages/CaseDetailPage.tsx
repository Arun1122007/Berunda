import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { useAuth } from "@/hooks/useAuth";
import { formatDate } from "@/lib";
import { ArrowLeft, AlertCircle, RefreshCw, Pencil, Trash2 } from "lucide-react";
import type { CaseDetail } from "@/types/api";

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

function DetailRow({ label, value }: { label: string; value: string | number | null | undefined }) {
  return (
    <div className="flex justify-between border-b border-surface-700 py-2 last:border-0">
      <span className="text-sm text-surface-400">{label}</span>
      <span className="text-sm font-medium text-surface-200">{value ?? "—"}</span>
    </div>
  );
}

function SectionCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Card header={<h3 className="font-semibold text-surface-100">{title}</h3>}>
      {children}
    </Card>
  );
}

export default function CaseDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const { isLoading: isDeleting, mutate: deleteCase } = useMutation<null>(
    `/fir/${id}`, "DELETE"
  );

  const { data: caseData, isLoading, error, refetch } = useQuery<CaseDetail>(
    `/fir/${id}`
  );

  const canEdit = user?.role === "admin" || user?.role === "officer";
  const canDelete = user?.role === "admin";

  const handleDelete = async () => {
    const result = await deleteCase(undefined);
    if (result !== null) {
      navigate("/cases", { replace: true });
    }
  };

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
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => navigate("/cases")}>
            <ArrowLeft size={16} /> Back to Cases
          </Button>
          <Button variant="secondary" onClick={refetch}>
            <RefreshCw size={16} /> Retry
          </Button>
        </div>
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-20">
        <AlertCircle size={20} className="text-surface-400" />
        <p className="text-surface-400">Case not found</p>
        <Button variant="secondary" onClick={() => navigate("/cases")}>
          <ArrowLeft size={16} /> Back to Cases
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate("/cases")}>
          <ArrowLeft size={16} /> Back
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-surface-100">
            Case {caseData.crimeNo || `#${caseData.caseMasterId}`}
          </h1>
          <p className="mt-1 text-sm text-surface-400">
            Registered {formatDate(caseData.crimeRegisteredDate)}
          </p>
        </div>
        <Badge variant={STATUS_COLOR[caseData.caseStatusId ?? 1] ?? "info"}>
          {STATUS_LABEL[caseData.caseStatusId ?? 1] ?? "Unknown"}
        </Badge>
        <div className="ml-auto flex gap-2">
          {canEdit && (
            <Button variant="secondary" size="sm" onClick={() => navigate(`/cases/${id}/edit`)}>
              <Pencil size={14} /> Edit
            </Button>
          )}
          {canDelete && (
            <Button variant="danger" size="sm" onClick={() => setShowDeleteConfirm(true)}>
              <Trash2 size={14} /> Delete
            </Button>
          )}
        </div>
      </div>

      {showDeleteConfirm && (
        <div className="rounded-lg border border-red-700 bg-red-900/20 p-4">
          <p className="text-sm text-red-300">
            Are you sure you want to delete this case? This action cannot be undone.
          </p>
          <div className="mt-3 flex gap-2">
            <Button variant="danger" size="sm" isLoading={isDeleting} onClick={handleDelete}>
              {isDeleting ? "Deleting..." : "Yes, Delete"}
            </Button>
            <Button variant="secondary" size="sm" onClick={() => setShowDeleteConfirm(false)}>
              Cancel
            </Button>
          </div>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <SectionCard title="Case Information">
          <DetailRow label="Crime No" value={caseData.crimeNo} />
          <DetailRow label="Case No" value={caseData.caseNo} />
          <DetailRow label="Registered Date" value={formatDate(caseData.crimeRegisteredDate)} />
          <DetailRow label="Police Station ID" value={caseData.policeStationId} />
          <DetailRow label="Status ID" value={caseData.caseStatusId} />
        </SectionCard>

        <SectionCard title="Crime Details">
          <DetailRow label="Major Head ID" value={caseData.crimeMajorHeadId} />
          <DetailRow label="Minor Head ID" value={caseData.crimeMinorHeadId} />
          <DetailRow label="Incident From" value={formatDate(caseData.incidentFromDate)} />
          <DetailRow label="Incident To" value={formatDate(caseData.incidentToDate)} />
        </SectionCard>
      </div>

      {caseData.latitude != null && caseData.longitude != null && (
        <SectionCard title="Location">
          <DetailRow label="Latitude" value={caseData.latitude.toFixed(6)} />
          <DetailRow label="Longitude" value={caseData.longitude.toFixed(6)} />
        </SectionCard>
      )}

      {caseData.briefFacts && (
        <SectionCard title="Brief Facts">
          <p className="whitespace-pre-wrap text-sm leading-relaxed text-surface-300">
            {caseData.briefFacts}
          </p>
        </SectionCard>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        {caseData.complainants && caseData.complainants.length > 0 && (
          <SectionCard title={`Complainants (${caseData.complainants.length})`}>
            <div className="space-y-3">
              {caseData.complainants.map((c: Record<string, unknown>, i: number) => (
                <div key={i} className="rounded-lg bg-surface-700/30 p-3">
                  <p className="text-sm font-medium text-surface-200">
                    {c.complainantName as string}
                  </p>
                  <p className="text-xs text-surface-400">
                    Age: {String(c.ageYear ?? "—")}
                  </p>
                </div>
              ))}
            </div>
          </SectionCard>
        )}

        {caseData.victims && caseData.victims.length > 0 && (
          <SectionCard title={`Victims (${caseData.victims.length})`}>
            <div className="space-y-3">
              {caseData.victims.map((v: Record<string, unknown>, i: number) => (
                <div key={i} className="rounded-lg bg-surface-700/30 p-3">
                  <p className="text-sm font-medium text-surface-200">
                    {v.victimName as string}
                  </p>
                  <p className="text-xs text-surface-400">
                    Age: {String(v.ageYear ?? "—")}
                  </p>
                </div>
              ))}
            </div>
          </SectionCard>
        )}

        {caseData.accused && caseData.accused.length > 0 && (
          <SectionCard title={`Accused (${caseData.accused.length})`}>
            <div className="space-y-3">
              {caseData.accused.map((a: Record<string, unknown>, i: number) => (
                <div key={i} className="rounded-lg bg-surface-700/30 p-3">
                  <p className="text-sm font-medium text-surface-200">
                    {a.accusedName as string}
                  </p>
                  <p className="text-xs text-surface-400">
                    Age: {String(a.ageYear ?? "—")}
                  </p>
                </div>
              ))}
            </div>
          </SectionCard>
        )}
      </div>
    </div>
  );
}
