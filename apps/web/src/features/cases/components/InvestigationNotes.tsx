import { useState } from "react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { Plus, FileText } from "lucide-react";
import type { InvestigationNote, InvestigationNoteCreate } from "@/types/api";

interface Props {
  caseMasterId: number;
}

export default function InvestigationNotes({ caseMasterId }: Props) {
  const [showForm, setShowForm] = useState(false);
  const [content, setContent] = useState("");
  const [noteType, setNoteType] = useState("general");

  const { data: notes, isLoading, refetch } = useQuery<InvestigationNote[]>(
    `/fir/${caseMasterId}/notes`
  );

  const { isLoading: isCreating, mutate: createNote } = useMutation<InvestigationNote>(
    `/fir/${caseMasterId}/notes`
  );

  const handleSubmit = async () => {
    if (!content.trim()) return;
    const result = await createNote({
      content,
      noteType,
    } as InvestigationNoteCreate);
    if (result) {
      setContent("");
      setShowForm(false);
      refetch();
    }
  };

  if (isLoading) return <LoadingSpinner size="sm" />;

  return (
    <Card header={
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-surface-100">Investigation Notes</h3>
        <Button variant="secondary" size="sm" onClick={() => setShowForm(!showForm)}>
          <Plus size={14} /> Add Note
        </Button>
      </div>
    }>
      {showForm && (
        <div className="mb-4 space-y-3 rounded-lg bg-surface-700/30 p-4">
          <select
            value={noteType}
            onChange={(e) => setNoteType(e.target.value)}
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200"
          >
            <option value="general">General</option>
            <option value="witness_statement">Witness Statement</option>
            <option value="forensic">Forensic</option>
            <option value="field_visit">Field Visit</option>
          </select>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter investigation note..."
            rows={4}
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200"
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

      {(!notes || notes.length === 0) ? (
        <div className="flex flex-col items-center justify-center py-8 text-surface-500">
          <FileText size={32} className="mb-2" />
          <p className="text-sm">No notes yet. Add the first investigation note.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {notes.map((note) => (
            <div key={note.noteId} className="rounded-lg border border-surface-700 bg-surface-800/30 p-3">
              <div className="mb-1 flex items-center gap-2">
                <span className="rounded bg-berunda-900/50 px-2 py-0.5 text-xs text-berunda-400">
                  {note.noteType || "general"}
                </span>
                {note.isAmendment && (
                  <span className="rounded bg-yellow-900/50 px-2 py-0.5 text-xs text-yellow-400">
                    Amendment
                  </span>
                )}
                <span className="ml-auto text-xs text-surface-500">
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
