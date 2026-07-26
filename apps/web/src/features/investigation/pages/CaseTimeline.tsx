import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { AlertCircle, RefreshCw, Clock, FileText, UserCheck, Eye, Search } from "lucide-react";
import Button from "@/components/ui/Button";
import type { TimelineEvent } from "@/types/api";

interface CaseTimelineProps {
  caseMasterId: number;
}

const EVENT_ICON: Record<string, React.ReactNode> = {
  FIR_REGISTERED: <FileText size={16} />,
  INVESTIGATION_NOTE: <Clock size={16} />,
  ASSIGNMENT: <UserCheck size={16} />,
  SUPERVISOR_REVIEW: <Eye size={16} />,
};

const EVENT_COLOR: Record<string, string> = {
  FIR_REGISTERED: "bg-blue-900/50 text-blue-400 border-blue-700",
  INVESTIGATION_NOTE: "bg-amber-900/50 text-amber-400 border-amber-700",
  ASSIGNMENT: "bg-green-900/50 text-green-400 border-green-700",
  SUPERVISOR_REVIEW: "bg-purple-900/50 text-purple-400 border-purple-700",
};

export default function CaseTimeline({ caseMasterId }: CaseTimelineProps) {
  const { data: timeline, isLoading, error, refetch } = useQuery<TimelineEvent[]>(
    `/fir/${caseMasterId}/timeline`
  );

  if (error) {
    return (
      <Card header={<h3 className="font-semibold text-surface-100">Case Timeline</h3>}>
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

  if (isLoading) {
    return (
      <Card header={<h3 className="font-semibold text-surface-100">Case Timeline</h3>}>
        <div className="flex justify-center py-8">
          <LoadingSpinner size="md" />
        </div>
      </Card>
    );
  }

  return (
    <Card header={<h3 className="font-semibold text-surface-100">Case Timeline</h3>}>
      {!timeline || timeline.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-surface-500">
          <Clock size={32} className="mb-2" />
          <p className="text-sm">No timeline events yet.</p>
        </div>
      ) : (
        <div className="relative space-y-0">
          {timeline.map((event, idx) => (
            <div key={idx} className="flex gap-4 pb-4 last:pb-0">
              <div className="flex flex-col items-center">
                <div
                  className={`flex h-8 w-8 items-center justify-center rounded-full border ${
                    EVENT_COLOR[event.type] || "bg-surface-700 text-surface-400 border-surface-600"
                  }`}
                >
                  {EVENT_ICON[event.type] || <Search size={14} />}
                </div>
                {idx < timeline.length - 1 && (
                  <div className="mt-1 h-full w-px bg-surface-700" />
                )}
              </div>
              <div className="min-w-0 flex-1 pt-1.5">
                <p className="text-sm font-medium text-surface-200">
                  {event.type.replace(/_/g, " ")}
                </p>
                {event.description && (
                  <p className="mt-0.5 text-xs text-surface-400">{event.description}</p>
                )}
                {event.timestamp && (
                  <p className="mt-0.5 text-xs text-surface-500">
                    {new Date(event.timestamp).toLocaleString()}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
