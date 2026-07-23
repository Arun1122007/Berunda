import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { CaseListResponse } from "@/types/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

const COLORS = ["#6366f1", "#f59e0b", "#ef4444", "#22c55e", "#3b82f6", "#ec4899"];

function countByCrimeHead(cases: { crimeMajorHeadId?: number | null }[]) {
  const counts: Record<string, number> = {};
  for (const c of cases) {
    const key = `Head ${c.crimeMajorHeadId ?? 0}`;
    counts[key] = (counts[key] || 0) + 1;
  }
  return Object.entries(counts).map(([name, count]) => ({ name, count }));
}

export default function AnalyticsPage() {
  const { data: firList, isLoading } = useQuery<CaseListResponse>("/fir?page_size=100");

  const chartData = firList ? countByCrimeHead(firList.items) : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Analytics</h1>
        <p className="mt-1 text-sm text-surface-400">
          Crime statistics, trends, and data visualisations
        </p>
      </div>

      {isLoading && <LoadingSpinner />}

      <div className="grid gap-6 lg:grid-cols-2">
        <Card
          header={
            <h2 className="font-semibold text-surface-100">
              Crime Type Distribution
            </h2>
          }
        >
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis
                dataKey="name"
                stroke="#94a3b8"
                tick={{ fill: "#94a3b8", fontSize: 12 }}
              />
              <YAxis
                stroke="#94a3b8"
                tick={{ fill: "#94a3b8", fontSize: 12 }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1e293b",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                  color: "#f1f5f9",
                }}
              />
              <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card
          header={
            <h2 className="font-semibold text-surface-100">
              District-wise Trends
            </h2>
          }
        >
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="count"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {chartData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </div>
  );
}
