import { useState, useRef } from "react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { Plus, Upload, FileIcon, AlertCircle, X } from "lucide-react";
import type { EvidenceMetadata } from "@/types/api";

interface Props {
  caseMasterId: number;
}

const EVIDENCE_TYPES = [
  "document",
  "photograph",
  "video",
  "audio",
  "forensic_report",
  "weapon",
  "digital",
  "other",
];

const STATUS_COLOR: Record<string, "info" | "warning" | "success" | "danger"> = {
  registered: "info",
  available: "success",
  under_review: "warning",
  restricted: "danger",
  archived: "info",
};

const SENSITIVITY_COLOR: Record<string, "info" | "warning" | "success" | "danger"> = {
  normal: "success",
  sensitive: "warning",
  restricted: "danger",
};

const ALLOWED_FILE_TYPES = [
  "application/pdf",
  "image/jpeg",
  "image/png",
  "image/tiff",
  "image/webp",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "video/mp4",
  "video/x-msvideo",
  "audio/mpeg",
  "audio/wav",
];

const ALLOWED_EXTENSIONS = ".pdf,.jpg,.jpeg,.png,.tiff,.webp,.doc,.docx,.mp4,.avi,.mp3,.wav";
const MAX_FILE_SIZE = 50 * 1024 * 1024;

export default function EvidenceManager({ caseMasterId }: Props) {
  const [showForm, setShowForm] = useState(false);
  const [evidenceType, setEvidenceType] = useState("document");
  const [description, setDescription] = useState("");
  const [source, setSource] = useState("");
  const [location, setLocation] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data: evidenceList, isLoading, error, refetch } = useQuery<EvidenceMetadata[]>(
    `/fir/${caseMasterId}/evidence`
  );

  const validateFile = (f: File): string | null => {
    if (!ALLOWED_FILE_TYPES.includes(f.type)) {
      return `Invalid file type: ${f.type || "unknown"}. Allowed: PDF, images, documents, video, audio.`;
    }
    if (f.size > MAX_FILE_SIZE) {
      return `File size exceeds 50 MB limit (${(f.size / (1024 * 1024)).toFixed(1)} MB).`;
    }
    return null;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    setFileError(null);
    if (selected) {
      const err = validateFile(selected);
      if (err) {
        setFileError(err);
        setFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
      } else {
        setFile(selected);
      }
    } else {
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setUploadProgress(0);
    setUploadError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("evidenceType", evidenceType);
      if (description) formData.append("description", description);
      if (source) formData.append("source", source);
      if (location) formData.append("location", location);

      const xhr = new XMLHttpRequest();
      xhr.upload.addEventListener("progress", (e) => {
        if (e.lengthComputable) {
          setUploadProgress(Math.round((e.loaded / e.total) * 100));
        }
      });

      const result = await new Promise<EvidenceMetadata>((resolve, reject) => {
        const token = localStorage.getItem("auth_token");
        xhr.open("POST", `/api/v1/fir/${caseMasterId}/evidence`);
        if (token) xhr.setRequestHeader("Authorization", `Bearer ${token}`);
        xhr.responseType = "json";
        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve(xhr.response);
          } else {
            const msg = xhr.response?.detail || `Upload failed (${xhr.status})`;
            reject(new Error(msg));
          }
        };
        xhr.onerror = () => reject(new Error("Network error during upload"));
        xhr.send(formData);
      });

      if (result) {
        setFile(null);
        setDescription("");
        setSource("");
        setLocation("");
        setEvidenceType("document");
        setShowForm(false);
        setUploadProgress(0);
        refetch();
      }
    } catch (err: unknown) {
      setUploadError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes: number | null): string => {
    if (bytes == null) return "—";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <Card header={<h3 className="font-semibold text-surface-100">Evidence</h3>}>
        <div className="flex flex-col items-center gap-3 py-8">
          <div className="flex items-center gap-2 text-red-400">
            <AlertCircle size={18} />
            <p className="text-sm">{error}</p>
          </div>
          <Button variant="secondary" size="sm" onClick={refetch}>Retry</Button>
        </div>
      </Card>
    );
  }

  return (
    <Card
      header={
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-surface-100">Evidence</h3>
          <Button variant="secondary" size="sm" onClick={() => setShowForm(!showForm)}>
            {showForm ? <X size={14} /> : <Plus size={14} />}
            {showForm ? "Cancel" : "Add Evidence"}
          </Button>
        </div>
      }
    >
      {showForm && (
        <div className="mb-6 space-y-4 rounded-lg border border-surface-700 bg-surface-800/50 p-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-surface-300">
                Evidence Type
              </label>
              <select
                value={evidenceType}
                onChange={(e) => setEvidenceType(e.target.value)}
                className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100"
              >
                {EVIDENCE_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {t.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-surface-300">
                Source
              </label>
              <input
                type="text"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                placeholder="e.g. IO collection, forensic lab"
                className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 placeholder-surface-500"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="mb-1.5 block text-sm font-medium text-surface-300">
                Description
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the evidence item"
                rows={2}
                className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 placeholder-surface-500"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="mb-1.5 block text-sm font-medium text-surface-300">
                Location / Seized From
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="e.g. Crime scene, suspect residence"
                className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 placeholder-surface-500"
              />
            </div>
          </div>

          <div className="border-t border-surface-700 pt-4">
            <label className="mb-1.5 block text-sm font-medium text-surface-300">
              Upload Evidence File
            </label>
            <input
              ref={fileInputRef}
              type="file"
              accept={ALLOWED_EXTENSIONS}
              onChange={handleFileChange}
              className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-200 file:mr-3 file:rounded file:border-0 file:bg-berunda-600 file:px-3 file:py-1 file:text-xs file:text-white"
            />
            <p className="mt-1 text-xs text-surface-500">
              Accepted: PDF, JPEG, PNG, TIFF, WebP, DOC, DOCX, MP4, AVI, MP3, WAV (max 50 MB)
            </p>
            {file && (
              <p className="mt-1 text-xs text-berunda-400">
                Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(1)} MB)
              </p>
            )}
            {fileError && (
              <div className="mt-1 flex items-center gap-1 text-xs text-red-400">
                <AlertCircle size={10} /> {fileError}
              </div>
            )}
          </div>

          {uploading && (
            <div className="space-y-1">
              <div className="flex items-center justify-between text-xs text-surface-400">
                <span>Uploading...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-surface-700">
                <div
                  className="h-full rounded-full bg-berunda-500 transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          )}

          {uploadError && (
            <div className="flex items-center gap-2 text-xs text-red-400">
              <AlertCircle size={12} /> {uploadError}
            </div>
          )}

          <div className="flex gap-2">
            <Button size="sm" isLoading={uploading} disabled={!file} onClick={handleUpload}>
              <Upload size={14} /> {uploading ? "Uploading..." : "Upload"}
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => {
                setShowForm(false);
                setFile(null);
                setFileError(null);
                setUploadError(null);
                setUploadProgress(0);
              }}
            >
              Cancel
            </Button>
          </div>
        </div>
      )}

      {(!evidenceList || evidenceList.length === 0) ? (
        <div className="flex flex-col items-center justify-center py-10 text-surface-500">
          <FileIcon size={36} className="mb-3" />
          <p className="text-sm">No evidence recorded for this case.</p>
          <p className="mt-1 text-xs text-surface-600">Click "Add Evidence" to upload or register evidence.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {evidenceList.map((ev) => (
            <div
              key={ev.evidenceId}
              className="flex items-start justify-between rounded-lg border border-surface-700 bg-surface-800/30 p-3"
            >
              <div className="min-w-0 flex-1">
                <div className="mb-1 flex items-center gap-2">
                  <span className="rounded bg-berunda-900/40 px-2 py-0.5 text-xs text-berunda-400">
                    {ev.evidenceType || "unknown"}
                  </span>
                  {ev.fileType && (
                    <span className="text-xs text-surface-500">{ev.fileType}</span>
                  )}
                  {ev.fileSize != null && (
                    <span className="text-xs text-surface-500">
                      ({formatFileSize(ev.fileSize)})
                    </span>
                  )}
                </div>
                <p className="truncate text-sm font-medium text-surface-200">
                  {ev.description || "No description"}
                </p>
                <div className="mt-1 flex flex-wrap gap-x-4 gap-y-1 text-xs text-surface-500">
                  {ev.source && <span>Source: {ev.source}</span>}
                  {ev.location && <span>Location: {ev.location}</span>}
                  {ev.createdAt && (
                    <span>{new Date(ev.createdAt).toLocaleString()}</span>
                  )}
                </div>
              </div>
              <div className="ml-3 flex flex-col items-end gap-1.5">
                <Badge variant={STATUS_COLOR[ev.status || "registered"] || "info"}>
                  {ev.status || "registered"}
                </Badge>
                {ev.sensitivity && (
                  <Badge variant={SENSITIVITY_COLOR[ev.sensitivity] || "info"}>
                    {ev.sensitivity}
                  </Badge>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
