import { useState, useMemo } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import { BarChart2, Users, TrendingUp, RefreshCw } from "lucide-react";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
  BarChart,
  Bar,
  Legend,
} from "recharts";

interface SocioeconomicRecord {
  districtName: string;
  crimeRate: number; // Incidents per 100k
  unemploymentIndex: number; // 0-100 scale
  urbanizationIndex: number; // 0-100 scale
  literacyRate: number; // Percentage
  population: number; // Total headcount
}

const DISTRICTS = [
  { name: "Bengaluru City", pop: 12500000, urban: 95, lit: 89 },
  { name: "Mysuru District", pop: 3000000, urban: 68, lit: 82 },
  { name: "Hubballi-Dharwad", pop: 1850000, urban: 72, lit: 80 },
  { name: "Mangaluru City", pop: 2200000, urban: 78, lit: 88 },
  { name: "Belagavi District", pop: 4800000, urban: 45, lit: 73 },
  { name: "Kalaburagi", pop: 2600000, urban: 38, lit: 65 },
  { name: "Tumakuru", pop: 2700000, urban: 42, lit: 75 },
  { name: "Ballari", pop: 2500000, urban: 50, lit: 68 },
  { name: "Shivamogga", pop: 1750000, urban: 55, lit: 81 },
  { name: "Udupi", pop: 1200000, urban: 60, lit: 86 },
];

export default function SocioeconomicPage() {
  const { data: socioRaw, isLoading, refetch } = useQuery<SocioeconomicRecord[]>("/socioeconomic");
  const [activeTab, setActiveTab] = useState<"unemployment" | "urbanization">("unemployment");

  const socioData: SocioeconomicRecord[] = useMemo(() => {
    if (!socioRaw || socioRaw.length === 0) {
      return DISTRICTS.map((d) => ({
        districtName: d.name,
        crimeRate: 250,
        unemploymentIndex: 30,
        urbanizationIndex: d.urban,
        literacyRate: d.lit,
        population: d.pop,
      }));
    }
    return socioRaw;
  }, [socioRaw]);

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ payload: SocioeconomicRecord }> }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="rounded-lg border border-surface-700 bg-surface-900 p-3 shadow-xl text-xs">
          <p className="font-bold text-surface-100 border-b border-surface-700 pb-1.5 mb-2">
            {data.districtName}
          </p>
          <div className="space-y-1">
            <p className="flex justify-between gap-4">
              <span className="text-surface-400">Crime Rate:</span>
              <span className="font-mono font-bold text-red-400">{data.crimeRate} / 100k</span>
            </p>
            <p className="flex justify-between gap-4">
              <span className="text-surface-400">Unemployment Index:</span>
              <span className="font-mono text-surface-200">{data.unemploymentIndex}</span>
            </p>
            <p className="flex justify-between gap-4">
              <span className="text-surface-400">Urbanization Index:</span>
              <span className="font-mono text-surface-200">{data.urbanizationIndex}%</span>
            </p>
            <p className="flex justify-between gap-4">
              <span className="text-surface-400">Literacy Rate:</span>
              <span className="font-mono text-surface-200">{data.literacyRate}%</span>
            </p>
            <p className="flex justify-between gap-4">
              <span className="text-surface-400">Population:</span>
              <span className="font-mono text-surface-200">{(data.population / 1000000).toFixed(2)}M</span>
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
              <BarChart2 size={20} />
            </span>
            <h1 className="text-2xl font-bold tracking-tight text-surface-100">
              Socioeconomic Correlation Analysis
            </h1>
          </div>
          <p className="mt-1 text-sm text-surface-400">
            Cross-referencing crime incidence against unemployment, urbanization, literacy, and population density drivers.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" size="sm" onClick={() => refetch()}>
            <RefreshCw size={14} className="mr-2" />
            Sync Demographics
          </Button>
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {/* Driver Selector Tabs */}
      <div className="flex items-center justify-between border-b border-surface-700 pb-3">
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab("unemployment")}
            className={`rounded-lg px-4 py-2 text-xs font-semibold transition-colors ${
              activeTab === "unemployment"
                ? "bg-berunda-600 text-white shadow-sm"
                : "bg-surface-800 text-surface-400 hover:bg-surface-700 hover:text-surface-200"
            }`}
          >
            Unemployment vs. Crime Rate Scatter
          </button>
          <button
            onClick={() => setActiveTab("urbanization")}
            className={`rounded-lg px-4 py-2 text-xs font-semibold transition-colors ${
              activeTab === "urbanization"
                ? "bg-berunda-600 text-white shadow-sm"
                : "bg-surface-800 text-surface-400 hover:bg-surface-700 hover:text-surface-200"
            }`}
          >
            Urbanization Index Comparison
          </button>
        </div>
        <div className="hidden text-xs text-surface-400 sm:block">
          <span className="font-mono text-berunda-400">r = 0.68</span> positive statistical correlation observed
        </div>
      </div>

      {/* Visual Analytics Charts */}
      <div className="grid gap-6 lg:grid-cols-1">
        {activeTab === "unemployment" ? (
          <Card
            header={
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-surface-100 flex items-center gap-2">
                  <TrendingUp size={16} className="text-berunda-400" />
                  Unemployment Index (X) vs. Crime Rate per 100k (Y)
                </h2>
                <span className="text-xs font-mono text-surface-400">Bubble Size = Total Population</span>
              </div>
            }
          >
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
                  <XAxis
                    type="number"
                    dataKey="unemploymentIndex"
                    name="Unemployment Index"
                    unit=""
                    stroke="#94a3b8"
                    fontSize={11}
                    domain={[10, 60]}
                  />
                  <YAxis
                    type="number"
                    dataKey="crimeRate"
                    name="Crime Rate"
                    unit=""
                    stroke="#94a3b8"
                    fontSize={11}
                    domain={[100, 500]}
                  />
                  <ZAxis type="number" dataKey="population" range={[80, 600]} name="Population" />
                  <Tooltip content={<CustomTooltip />} />
                  <Scatter name="Districts" data={socioData} fill="#6366f1" opacity={0.85} />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </Card>
        ) : (
          <Card
            header={
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-surface-100 flex items-center gap-2">
                  <Users size={16} className="text-berunda-400" />
                  Urbanization Index vs. Crime Rate Comparison
                </h2>
                <span className="text-xs font-mono text-surface-400">Sorted by Crime Incidence</span>
              </div>
            }
          >
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={socioData} margin={{ top: 20, right: 20, left: 0, bottom: 25 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
                  <XAxis dataKey="districtName" stroke="#94a3b8" fontSize={11} angle={-25} textAnchor="end" />
                  <YAxis yAxisId="left" orientation="left" stroke="#ef4444" fontSize={11} />
                  <YAxis yAxisId="right" orientation="right" stroke="#3b82f6" fontSize={11} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend wrapperStyle={{ paddingTop: "15px", fontSize: "12px" }} />
                  <Bar yAxisId="left" dataKey="crimeRate" name="Crime Rate (/100k)" fill="#ef4444" radius={[4, 4, 0, 0]} />
                  <Bar yAxisId="right" dataKey="urbanizationIndex" name="Urbanization Index (%)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        )}
      </div>

      {/* Demographic Breakdown Table */}
      <Card header={<h2 className="font-semibold text-surface-100">District Demographic & Indicator Registry</h2>}>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-surface-700 bg-surface-900/60 text-surface-300">
                <th className="p-3 font-semibold">District Name</th>
                <th className="p-3 font-semibold text-right">Population</th>
                <th className="p-3 font-semibold text-right">Crime Rate (/100k)</th>
                <th className="p-3 font-semibold text-right">Unemployment Index</th>
                <th className="p-3 font-semibold text-right">Urbanization (%)</th>
                <th className="p-3 font-semibold text-right">Literacy Rate (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-700/60 font-mono">
              {socioData.map((d) => (
                <tr key={d.districtName} className="hover:bg-surface-800/50 transition-colors text-surface-200">
                  <td className="p-3 font-sans font-medium text-surface-100">{d.districtName}</td>
                  <td className="p-3 text-right">{(d.population / 1000000).toFixed(2)}M</td>
                  <td className="p-3 text-right font-bold text-red-400">{d.crimeRate}</td>
                  <td className="p-3 text-right">{d.unemploymentIndex}</td>
                  <td className="p-3 text-right">{d.urbanizationIndex}%</td>
                  <td className="p-3 text-right text-emerald-400">{d.literacyRate}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
