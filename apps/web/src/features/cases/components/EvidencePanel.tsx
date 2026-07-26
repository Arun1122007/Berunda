import { useState } from "react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { apiClient } from "@/services/api-client";
import { Plus, FileIcon, Upload, AlertCircle } from "lucide-react";
import type { EvidenceItem } from "@/types/api";

interface Props {
  caseMasterId: number;
}

const EVIDENCE_STATUS_COLOR: Record<string, "info" | "warning" | "success" | "danger"> = {
  registered: "info",
  uploading: "warning",
  available: "success",
  under_review: "warning",
  restricted: "danger",
  archived: "info",
};

export default function EvidencePanel({ caseMasterId }: Props) {
  const [showUpload, setShowUpload] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [description, setDescription] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const { data: evidenceList, isLoading, refetch } = useQuery<EvidenceItem[]>(
    `/fir/${caseMasterId}/evidence`
  );

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setUploadError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      if (description) formData.append("description", description);
      await apiClient.upload(`/fir/${caseMasterId}/evidence`, formData);
      setFile(null);
      setDescription("");
      setShowUpload(false);
      refetch();
    } catch (err: unknown) {
      setUploadError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="sm" />;

  return (
    <Card header={
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-surface-100">Evidence</h3>
        <Button variant="secondary" size="sm" onClick={() => setShowUpload(!showUpload)}>
          <Plus size={14} /> Add Evidence
        </Button>
      </div>
    }>
      {showUpload && (
        <div className="mb-4 space-y-3 rounded-lg border border-surface-700 bg-surface-800/30 p-4">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200 file:mr-3 file:rounded file:border-0 file:bg-berunda-600 file:px-3 file:py-1 file:text-xs file:text-white"
          />
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Evidence description (optional)"
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200"
          />
          {uploadError && (
            <div className="flex items-center gap-2 text-xs text-red-400">
              <AlertCircle size={12} /> {uploadError}
            </div>
          )}
          <div className="flex gap-2">
            <Button size="sm" isLoading={uploading} onClick={handleUpload}>
              <Upload size={14} /> Upload
            </Button>
            <Button variant="secondary" size="sm" onClick={() => setShowUpload(false)}>
              Cancel
            </Button>
          </div>
        </div>
      )}

      {(!evidenceList || evidenceList.length === 0) ? (
        <div className="flex flex-col items-center justify-center py-8 text-surface-500">
          <FileIcon size={32} className="mb-2" />
          <p className="text-sm">No evidence uploaded yet.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {evidenceList.map((ev) => (
            <div key={ev.evidenceId} className="flex items-center justify-between rounded-lg border border-surface-700 bg-surface-800/30 p-3">
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-surface-200">
                  {ev.description || "No description"}
                </p>
                <p className="text-xs text-surface-500">
                  {ev.evidenceType || "unknown type"} &middot; {ev.createdAt ? new Date(ev.createdAt).toLocaleDateString() : ""}
                </p>
              </div>
              <div className="ml-3 flex items-center gap-2">
                <Badge variant={EVIDENCE_STATUS_COLOR[ev.status || "registered"] || "info"}>
                  {ev.status || "registered"}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
