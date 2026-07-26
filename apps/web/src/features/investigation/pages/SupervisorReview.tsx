import { useState } from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { Plus, AlertCircle, RefreshCw, Eye } from "lucide-react";
import type { SupervisorReview } from "@/types/api";

interface SupervisorReviewProps {
  caseMasterId: number;
  isSupervisor: boolean;
}

const REVIEW_TYPE_COLOR: Record<string, "info" | "warning" | "success" | "default"> = {
  periodic: "info",
  evidence_review: "warning",
  progress_review: "success",
};

const STATUS_COLOR: Record<string, "info" | "warning" | "success" | "danger"> = {
  pending: "warning",
  approved: "success",
  changes_requested: "danger",
};

const REVIEW_TYPE_OPTIONS = [
  { value: "periodic", label: "Periodic" },
  { value: "evidence_review", label: "Evidence Review" },
  { value: "progress_review", label: "Progress Review" },
];

const STATUS_OPTIONS = [
  { value: "pending", label: "Pending" },
  { value: "approved", label: "Approved" },
  { value: "changes_requested", label: "Changes Requested" },
];

export default function SupervisorReview({ caseMasterId, isSupervisor }: SupervisorReviewProps) {
  const [showForm, setShowForm] = useState(false);
  const [reviewType, setReviewType] = useState("periodic");
  const [status, setStatus] = useState("pending");
  const [comments, setComments] = useState("");

  const { data: reviews, isLoading, error, refetch } = useQuery<SupervisorReview[]>(
    `/fir/${caseMasterId}/reviews`
  );

  const { isLoading: isCreating, mutate: createReview } = useMutation<SupervisorReview>(
    `/fir/${caseMasterId}/reviews`
  );

  const handleSubmit = async () => {
    if (!comments.trim()) return;
    const result = await createReview({
      reviewType,
      status,
      comments: comments.trim(),
    });
    if (result) {
      setComments("");
      setReviewType("periodic");
      setStatus("pending");
      setShowForm(false);
      refetch();
    }
  };

  if (error) {
    return (
      <Card header={<h3 className="font-semibold text-surface-100">Supervisor Reviews</h3>}>
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
          <h3 className="font-semibold text-surface-100">Supervisor Reviews</h3>
          {isSupervisor && (
            <Button variant="secondary" size="sm" onClick={() => setShowForm(!showForm)} disabled={isLoading}>
              <Plus size={14} /> New Review
            </Button>
          )}
        </div>
      }
    >
      {showForm && isSupervisor && (
        <div className="mb-4 space-y-3 rounded-lg bg-surface-700/30 p-4">
          <div className="grid grid-cols-2 gap-3">
            <select
              value={reviewType}
              onChange={(e) => setReviewType(e.target.value)}
              className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200"
            >
              {REVIEW_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200"
            >
              {STATUS_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <textarea
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            placeholder="Review comments..."
            rows={4}
            className="w-full rounded-lg border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-surface-200 placeholder-surface-500"
          />
          <div className="flex gap-2">
            <Button size="sm" isLoading={isCreating} onClick={handleSubmit}>
              Submit Review
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
      ) : !reviews || reviews.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-surface-500">
          <Eye size={32} className="mb-2" />
          <p className="text-sm">No reviews yet.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {reviews.map((review) => (
            <div key={review.reviewId} className="rounded-lg border border-surface-700 bg-surface-800/30 p-3">
              <div className="mb-1 flex items-center gap-2">
                <Badge variant={REVIEW_TYPE_COLOR[review.reviewType || "periodic"] || "info"}>
                  {review.reviewType?.replace(/_/g, " ") || "Periodic"}
                </Badge>
                <Badge variant={STATUS_COLOR[review.status || "pending"] || "info"}>
                  {review.status?.replace(/_/g, " ") || "Pending"}
                </Badge>
                <span className="ml-auto text-xs text-surface-500">
                  {review.supervisorId && `by User #${review.supervisorId} `}
                  {review.reviewedAt ? new Date(review.reviewedAt).toLocaleString() : ""}
                </span>
              </div>
              {review.comments && (
                <p className="whitespace-pre-wrap text-sm text-surface-300">{review.comments}</p>
              )}
              {review.actionRequested && (
                <p className="mt-1 text-xs text-amber-400">Action: {review.actionRequested}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
