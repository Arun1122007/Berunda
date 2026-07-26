import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { apiClient } from "@/services/api-client";
import { RefreshCw, Link2, ThumbsUp, ThumbsDown, AlertCircle } from "lucide-react";
import type { RelatedCaseSuggestionResponse } from "@/types/api";

interface Props {
  caseMasterId: number;
}

const REVIEW_STATUS_COLOR: Record<string, "info" | "warning" | "success" | "danger" | "default"> = {
  suggested: "info",
  under_review: "warning",
  accepted: "success",
  rejected: "danger",
  superseded: "default",
};

function getConfidenceColor(score: number): string {
  if (score >= 0.8) return "bg-green-500";
  if (score >= 0.5) return "bg-yellow-500";
  return "bg-red-500";
}

export default function RelatedCasesPanel({ caseMasterId }: Props) {
  const navigate = useNavigate();
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [reviewReason, setReviewReason] = useState("");
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const { data: suggestions, isLoading, error, refetch } = useQuery<RelatedCaseSuggestionResponse[]>(
    `/fir/${caseMasterId}/related-cases`
  );

  const { isLoading: isGenerating, mutate: generate } = useMutation<RelatedCaseSuggestionResponse[]>(
    `/fir/${caseMasterId}/related-cases/generate`
  );

  const handleGenerate = async () => {
    await generate(undefined);
    refetch();
  };

  const handleReview = async (suggestionId: number, reviewStatus: "accepted" | "rejected") => {
    setUpdatingId(suggestionId);
    try {
      await apiClient.put(`/fir/related-cases/${suggestionId}/review`, {
        reviewStatus,
        reviewReason: reviewReason || undefined,
      });
      setReviewReason("");
      setExpandedId(null);
      refetch();
    } catch {
      // handled by api client
    } finally {
      setUpdatingId(null);
    }
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
      <Card header={<h3 className="font-semibold text-surface-100">Related Cases</h3>}>
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
          <h3 className="font-semibold text-surface-100">Related Cases</h3>
          <Button
            variant="secondary"
            size="sm"
            isLoading={isGenerating}
            onClick={handleGenerate}
          >
            <RefreshCw size={14} />
            {suggestions && suggestions.length > 0 ? "Refresh" : "Find Related"}
          </Button>
        </div>
      }
    >
      {(!suggestions || suggestions.length === 0) ? (
        <div className="flex flex-col items-center justify-center py-10 text-surface-500">
          <Link2 size={36} className="mb-3" />
          <p className="text-sm">No related cases found.</p>
          <p className="mt-1 text-xs text-surface-600">
            Click "Find Related" to search for linked cases using the AI model.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {suggestions.map((s) => (
            <div
              key={s.suggestionId}
              className="rounded-lg border border-surface-700 bg-surface-800/30 p-3"
            >
              <div className="mb-2 flex items-center justify-between">
                <button
                  className="text-sm font-medium text-berunda-400 hover:text-berunda-300"
                  onClick={() => navigate(`/cases/${s.candidateFIRId}`)}
                >
                  {s.candidateCrimeNo || `Case #${s.candidateFIRId}`}
                </button>
                <Badge
                  variant={REVIEW_STATUS_COLOR[s.reviewStatus || "suggested"] || "info"}
                >
                  {s.reviewStatus || "suggested"}
                </Badge>
              </div>

              <div className="mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-surface-500">Confidence:</span>
                  <div className="h-2 w-28 overflow-hidden rounded-full bg-surface-700">
                    <div
                      className={`h-full rounded-full transition-all ${getConfidenceColor(s.confidenceScore)}`}
                      style={{ width: `${Math.round(s.confidenceScore * 100)}%` }}
                    />
                  </div>
                  <span className="text-xs font-medium text-surface-400">
                    {Math.round(s.confidenceScore * 100)}%
                  </span>
                </div>
              </div>

              {s.explanation && (
                <p className="mb-1 text-xs leading-relaxed text-surface-400">
                  {s.explanation}
                </p>
              )}

              {s.supportingSignals && (
                <div className="mb-2">
                  <span className="text-xs text-surface-500">Signals: </span>
                  <span className="text-xs text-surface-400">{s.supportingSignals}</span>
                </div>
              )}

              {s.reviewStatus === "suggested" && (
                <div className="mt-3 space-y-2">
                  {expandedId === s.suggestionId ? (
                    <>
                      <textarea
                        value={reviewReason}
                        onChange={(e) => setReviewReason(e.target.value)}
                        placeholder="Review reason (optional)"
                        rows={2}
                        className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 placeholder-surface-500"
                      />
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="secondary"
                          isLoading={updatingId === s.suggestionId}
                          onClick={() => handleReview(s.suggestionId, "accepted")}
                        >
                          <ThumbsUp size={12} /> Accept
                        </Button>
                        <Button
                          size="sm"
                          variant="secondary"
                          isLoading={updatingId === s.suggestionId}
                          onClick={() => handleReview(s.suggestionId, "rejected")}
                        >
                          <ThumbsDown size={12} /> Reject
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => {
                            setExpandedId(null);
                            setReviewReason("");
                          }}
                        >
                          Cancel
                        </Button>
                      </div>
                    </>
                  ) : (
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => setExpandedId(s.suggestionId)}
                    >
                      Review Suggestion
                    </Button>
                  )}
                </div>
              )}

              {s.reviewReason && (
                <p className="mt-1 text-xs text-surface-500">
                  Reason: {s.reviewReason}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
