import { useState } from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { Sparkles, Check, X, Edit3, ShieldCheck } from "lucide-react";

interface AISuggestionItem {
  field_name: string;
  original_value?: string;
  suggested_value: string;
  confidence: number;
  reasoning: string;
}

interface AISuggestion {
  ExtractionID: number;
  CaseMasterID: number;
  Status: "PENDING" | "APPROVED" | "REJECTED" | "MODIFIED";
  Suggestions: AISuggestionItem[];
  ConfidenceScore: number;
  ReviewedBy?: number;
  ReviewComments?: string;
}

export default function AIReviewPanel({ caseMasterId }: { caseMasterId: number }) {
  const [editingField, setEditingField] = useState<string | null>(null);
  const [customValues, setCustomValues] = useState<Record<string, string>>({});
  const [reviewComment, setReviewComment] = useState("");
  const [actionStatus, setActionStatus] = useState<string | null>(null);

  const { data: suggestions, isLoading, refetch } = useQuery<AISuggestion[]>(
    `/assistant/suggestions?case_master_id=${caseMasterId}`
  );

  const { mutate: applyMutation, isLoading: isApplying } = useMutation<any>(
    suggestions && suggestions.length > 0 ? `/assistant/suggestions/${suggestions[0].ExtractionID}/apply` : "",
    "POST"
  );

  const { mutate: rejectMutation, isLoading: isRejecting } = useMutation<any>(
    suggestions && suggestions.length > 0 ? `/assistant/suggestions/${suggestions[0].ExtractionID}/reject` : "",
    "POST"
  );

  if (isLoading) {
    return (
      <Card header={<div className="flex items-center gap-2 font-semibold text-primary-400"><Sparkles className="h-5 w-5" /> AI Investigation & Extraction Suggestions</div>}>
        <div className="flex justify-center py-6"><LoadingSpinner /></div>
      </Card>
    );
  }

  const suggestion = suggestions && suggestions.length > 0 ? suggestions[0] : null;

  if (!suggestion) {
    return (
      <Card header={<div className="flex items-center gap-2 font-semibold text-primary-400"><Sparkles className="h-5 w-5" /> AI Investigation & Extraction Suggestions</div>}>
        <p className="text-sm text-surface-400 py-4">No AI extraction suggestions pending or generated for this case yet.</p>
      </Card>
    );
  }

  const statusBadgeMap: Record<string, { label: string; variant: "warning" | "success" | "danger" | "info" }> = {
    PENDING: { label: "Pending Review", variant: "warning" },
    APPROVED: { label: "Applied", variant: "success" },
    REJECTED: { label: "Rejected", variant: "danger" },
    MODIFIED: { label: "Modified", variant: "info" },
  };

  const currentStatus = statusBadgeMap[suggestion.Status] || { label: suggestion.Status, variant: "info" };

  const handleApply = async () => {
    setActionStatus(null);
    try {
      await applyMutation({ comments: reviewComment || "Applied via AI Review Panel", modified_fields: customValues });
      setActionStatus("Suggestion successfully applied to case record.");
      refetch();
    } catch (err: any) {
      setActionStatus(err?.message || "Failed to apply suggestion.");
    }
  };

  const handleReject = async () => {
    setActionStatus(null);
    try {
      await rejectMutation({ comments: reviewComment || "Rejected via AI Review Panel" });
      setActionStatus("Suggestion rejected and archived.");
      refetch();
    } catch (err: any) {
      setActionStatus(err?.message || "Failed to reject suggestion.");
    }
  };

  return (
    <Card
      header={
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 font-semibold text-primary-400">
            <Sparkles className="h-5 w-5 text-amber-400" />
            AI Extraction & Review Panel
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-surface-400">Overall Confidence:</span>
            <Badge variant={suggestion.ConfidenceScore >= 0.8 ? "success" : "warning"}>
              {Math.round(suggestion.ConfidenceScore * 100)}%
            </Badge>
            <Badge variant={currentStatus.variant}>{currentStatus.label}</Badge>
          </div>
        </div>
      }
    >
      <div className="space-y-4">
        <div className="bg-surface-800/60 p-3 rounded-lg border border-surface-700 flex items-start gap-3">
          <ShieldCheck className="h-5 w-5 text-primary-400 shrink-0 mt-0.5" />
          <div className="text-xs text-surface-300">
            <p className="font-semibold text-surface-200">Immutable Original Source Preservation</p>
            AI suggestions never overwrite original FIR data automatically. Reviewers must verify reasoning and confidence scores before applying or modifying extracted values.
          </div>
        </div>

        {actionStatus && (
          <div className="p-3 rounded-lg bg-primary-950/40 border border-primary-500/30 text-xs text-primary-300">
            {actionStatus}
          </div>
        )}

        <div className="border border-surface-700 rounded-lg overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-800 border-b border-surface-700 text-xs text-surface-400 uppercase font-medium">
                <th className="p-3">Field Name</th>
                <th className="p-3">Original Data</th>
                <th className="p-3">AI Suggested Value</th>
                <th className="p-3">Confidence & Rationale</th>
                <th className="p-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-700/60 text-sm">
              {suggestion.Suggestions?.map((item, idx) => {
                const isEditing = editingField === item.field_name;
                const displayVal = customValues[item.field_name] !== undefined ? customValues[item.field_name] : item.suggested_value;
                return (
                  <tr key={idx} className="hover:bg-surface-800/30 transition-colors">
                    <td className="p-3 font-medium text-surface-200">{item.field_name}</td>
                    <td className="p-3 text-surface-400">{item.original_value || "— (Not Set)"}</td>
                    <td className="p-3 font-semibold text-primary-300">
                      {isEditing ? (
                        <input
                          type="text"
                          className="bg-surface-900 border border-surface-600 rounded px-2 py-1 text-xs text-surface-100 w-full focus:outline-none focus:border-primary-500"
                          value={displayVal}
                          onChange={(e) => setCustomValues({ ...customValues, [item.field_name]: e.target.value })}
                        />
                      ) : (
                        displayVal
                      )}
                    </td>
                    <td className="p-3 text-xs">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`font-semibold ${item.confidence >= 0.8 ? "text-emerald-400" : "text-amber-400"}`}>
                          {Math.round(item.confidence * 100)}% Conf.
                        </span>
                      </div>
                      <p className="text-surface-400 text-xs">{item.reasoning}</p>
                    </td>
                    <td className="p-3 text-right">
                      {suggestion.Status === "PENDING" && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setEditingField(isEditing ? null : item.field_name)}
                          title="Edit Before Apply"
                        >
                          <Edit3 className="h-4 w-4 text-surface-300 hover:text-primary-400" />
                        </Button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {suggestion.Status === "PENDING" && (
          <div className="space-y-3 pt-2 border-t border-surface-700">
            <div>
              <label className="block text-xs font-medium text-surface-400 mb-1">
                Reviewer Comments / Audit Note (Optional)
              </label>
              <input
                type="text"
                placeholder="Enter verification notes or reason for rejection..."
                className="w-full bg-surface-900 border border-surface-700 rounded-lg px-3 py-2 text-sm text-surface-200 focus:outline-none focus:border-primary-500"
                value={reviewComment}
                onChange={(e) => setReviewComment(e.target.value)}
              />
            </div>
            <div className="flex justify-end gap-3">
              <Button
                variant="danger"
                size="sm"
                onClick={handleReject}
                disabled={isRejecting || isApplying}
              >
                <X className="h-4 w-4 mr-1.5" /> Reject Suggestion
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={handleApply}
                disabled={isApplying || isRejecting}
              >
                <Check className="h-4 w-4 mr-1.5" /> Apply Suggestion
              </Button>
            </div>
          </div>
        )}

        {suggestion.ReviewComments && (
          <div className="text-xs text-surface-400 bg-surface-900/50 p-2.5 rounded border border-surface-700">
            <span className="font-semibold text-surface-300">Review Note:</span> {suggestion.ReviewComments}
          </div>
        )}
      </div>
    </Card>
  );
}
