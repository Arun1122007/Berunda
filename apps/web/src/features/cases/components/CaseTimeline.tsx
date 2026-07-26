import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { Clock, FileText, UserCheck, Search, Eye } from "lucide-react";
import type { TimelineEvent } from "@/types/api";

interface Props {
  caseMasterId: number;
}

const EVENT_ICON: Record<string, React.ReactNode> = {
  FIR_REGISTERED: <FileText size={14} />,
  INVESTIGATION_NOTE: <Clock size={14} />,
  ASSIGNMENT: <UserCheck size={14} />,
  SUPERVISOR_REVIEW: <Eye size={14} />,
};

export default function CaseTimeline({ caseMasterId }: Props) {
  const { data: timeline, isLoading } = useQuery<TimelineEvent[]>(
    `/fir/${caseMasterId}/timeline`
  );

  if (isLoading) return <LoadingSpinner size="sm" />;

  return (
    <Card header={<h3 className="font-semibold text-surface-100">Case Timeline</h3>}>
      {(!timeline || timeline.length === 0) ? (
        <p className="py-4 text-center text-sm text-surface-500">No timeline events yet.</p>
      ) : (
        <div className="relative space-y-0">
          {timeline.map((event, idx) => (
            <div key={idx} className="flex gap-4 pb-4">
              <div className="flex flex-col items-center">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-surface-700 text-surface-400">
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
