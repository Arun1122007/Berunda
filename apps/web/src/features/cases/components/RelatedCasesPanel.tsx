import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { apiClient } from "@/services/api-client";
import { RefreshCw, Link2, ThumbsUp, ThumbsDown } from "lucide-react";
import type { RelatedCaseSuggestion } from "@/types/api";

interface Props {
  caseMasterId: number;
}

export default function RelatedCasesPanel({ caseMasterId }: Props) {
  const navigate = useNavigate();
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  const { data: suggestions, isLoading, refetch } = useQuery<RelatedCaseSuggestion[]>(
    `/fir/${caseMasterId}/related-cases`
  );

  const { isLoading: isGenerating, mutate: generate } = useMutation<RelatedCaseSuggestion[]>(
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
      });
      refetch();
    } catch {
      // handled by api client
    } finally {
      setUpdatingId(null);
    }
  };

  if (isLoading) return <LoadingSpinner size="sm" />;

  return (
    <Card header={
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-surface-100">Related Cases</h3>
        <Button variant="secondary" size="sm" isLoading={isGenerating} onClick={handleGenerate}>
          <RefreshCw size={14} /> {suggestions && suggestions.length > 0 ? "Refresh" : "Find Related"}
        </Button>
      </div>
    }>
      {(!suggestions || suggestions.length === 0) ? (
        <div className="flex flex-col items-center justify-center py-8 text-surface-500">
          <Link2 size={32} className="mb-2" />
          <p className="text-sm">No related cases found. Click "Find Related" to search.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {suggestions.map((s) => (
            <div key={s.suggestionId} className="rounded-lg border border-surface-700 bg-surface-800/30 p-3">
              <div className="mb-2 flex items-center justify-between">
                <button
                  className="text-sm font-medium text-berunda-400 hover:text-berunda-300"
                  onClick={() => navigate(`/cases/${s.candidateFirId}`)}
                >
                  {s.candidateCrimeNo || `Case #${s.candidateFirId}`}
                </button>
                <Badge variant={
                  s.reviewStatus === "accepted" ? "success" :
                  s.reviewStatus === "rejected" ? "danger" : "info"
                }>
                  {s.reviewStatus || "suggested"}
                </Badge>
              </div>

              <div className="mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-surface-500">Confidence:</span>
                  <div className="h-2 w-24 overflow-hidden rounded-full bg-surface-700">
                    <div
                      className="h-full rounded-full bg-berunda-500"
                      style={{ width: `${Math.round(s.confidenceScore * 100)}%` }}
                    />
                  </div>
                  <span className="text-xs text-surface-400">{Math.round(s.confidenceScore * 100)}%</span>
                </div>
              </div>

              {s.explanation && (
                <p className="mb-2 text-xs text-surface-400">{s.explanation}</p>
              )}

              {s.reviewStatus === "suggested" && (
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
                </div>
              )}

              {s.reviewReason && (
                <p className="mt-1 text-xs text-surface-500">Reason: {s.reviewReason}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
