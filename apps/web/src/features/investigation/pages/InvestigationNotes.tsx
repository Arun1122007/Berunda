import { useState } from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { Plus, FileText, AlertCircle, RefreshCw } from "lucide-react";
import type { InvestigationNote, InvestigationNoteCreate } from "@/types/api";

interface InvestigationNotesProps {
  caseMasterId: number;
}

const NOTE_TYPE_COLOR: Record<string, "info" | "warning" | "success" | "danger" | "default"> = {
  general: "default",
  witness_statement: "success",
  forensic: "warning",
  field_visit: "info",
};

const NOTE_TYPE_OPTIONS = [
  { value: "general", label: "General" },
  { value: "witness_statement", label: "Witness Statement" },
  { value: "forensic", label: "Forensic" },
  { value: "field_visit", label: "Field Visit" },
];

const VISIBILITY_OPTIONS = [
  { value: "station", label: "Station" },
  { value: "supervisor", label: "Supervisor" },
  { value: "private", label: "Private" },
];

export default function InvestigationNotes({ caseMasterId }: InvestigationNotesProps) {
  const [showForm, setShowForm] = useState(false);
  const [content, setContent] = useState("");
  const [noteType, setNoteType] = useState("general");
  const [visibility, setVisibility] = useState("station");

  const { data: notes, isLoading, error, refetch } = useQuery<InvestigationNote[]>(
    `/fir/${caseMasterId}/notes`
  );

  const { isLoading: isCreating, mutate: createNote } = useMutation<InvestigationNote>(
    `/fir/${caseMasterId}/notes`
  );

  const handleSubmit = async () => {
    if (!content.trim()) return;
    const result = await createNote({
      content: content.trim(),
      noteType,
      visibility,
    } as InvestigationNoteCreate);
    if (result) {
      setContent("");
      setNoteType("general");
      setVisibility("station");
      setShowForm(false);
      refetch();
    }
  };

  if (error) {
    return (
      <Card header={<h3 className="font-semibold text-surface-100">Investigation Notes</h3>}>
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
          <h3 className="font-semibold text-surface-100">Investigation Notes</h3>
          <Button variant="secondary" size="sm" onClick={() => setShowForm(!showForm)} disabled={isLoading}>
            <Plus size={14} /> Add Note
          </Button>
        </div>
      }
    >
      {showForm && (
        <div className="mb-4 space-y-3 rounded-lg bg-surface-700/30 p-4">
          <div className="grid grid-cols-2 gap-3">
            <select
              value={noteType}
              onChange={(e) => setNoteType(e.target.value)}
              className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200"
            >
              {NOTE_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
            <select
              value={visibility}
              onChange={(e) => setVisibility(e.target.value)}
              className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200"
            >
              {VISIBILITY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter investigation note..."
            rows={4}
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200 placeholder-surface-500"
          />
          <div className="flex gap-2">
            <Button size="sm" isLoading={isCreating} onClick={handleSubmit}>
              Save Note
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
      ) : !notes || notes.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-surface-500">
          <FileText size={32} className="mb-2" />
          <p className="text-sm">No notes yet. Add the first investigation note.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {notes.map((note) => (
            <div key={note.noteId} className="rounded-lg border border-surface-700 bg-surface-800/30 p-3">
              <div className="mb-1 flex items-center gap-2">
                <Badge variant={NOTE_TYPE_COLOR[note.noteType || "general"] || "default"}>
                  {note.noteType?.replace(/_/g, " ") || "General"}
                </Badge>
                {note.visibility && (
                  <span className="rounded bg-surface-700 px-2 py-0.5 text-xs text-surface-400">
                    {note.visibility}
                  </span>
                )}
                {note.isAmendment && (
                  <Badge variant="warning">Amendment</Badge>
                )}
                <span className="ml-auto text-xs text-surface-500">
                  {note.authorId && `by User #${note.authorId} `}
                  {note.createdAt ? new Date(note.createdAt).toLocaleString() : ""}
                </span>
              </div>
              <p className="whitespace-pre-wrap text-sm text-surface-300">{note.content}</p>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
