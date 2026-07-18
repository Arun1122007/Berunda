import Card from "@/components/ui/Card";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const sampleData = [
  { name: "Theft", count: 45 },
  { name: "Assault", count: 32 },
  { name: "Burglary", count: 28 },
  { name: "Robbery", count: 21 },
  { name: "Fraud", count: 17 },
  { name: "Homicide", count: 8 },
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Analytics</h1>
        <p className="mt-1 text-sm text-surface-400">
          Crime statistics, trends, and data visualisations
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card
          header={
            <h2 className="font-semibold text-surface-100">
              Crime Type Distribution
            </h2>
          }
        >
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sampleData}>
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
          <p className="py-12 text-center text-sm text-surface-500">
            Select a district to view trends
          </p>
        </Card>
      </div>
    </div>
  );
}
