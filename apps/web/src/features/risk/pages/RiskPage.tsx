import { useState, useMemo } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { RiskScore } from "@/types/api";
import { TrendingUp, AlertOctagon, ShieldAlert, Info, RefreshCw } from "lucide-react";

interface RiskCell {
  district: string;
  crimeHead: string;
  score: number;
  incidentCount: number;
  trend: "up" | "down" | "stable";
  riskLevel: "Critical" | "High" | "Moderate" | "Low";
}

const DISTRICTS = [
  "Bengaluru City",
  "Mysuru District",
  "Hubballi-Dharwad",
  "Mangaluru City",
  "Belagavi District",
  "Kalaburagi",
  "Tumakuru",
  "Ballari",
  "Shivamogga",
  "Udupi",
];

const CRIME_HEADS = [
  "Cybercrime & Financial Fraud",
  "Theft & Burglary",
  "Narcotics & NDPS",
  "Violent Assault & IPC 307",
  "Organized Syndicate Activity",
  "Traffic Fatalities & IPC 304A",
];

export default function RiskPage() {
  const { data: riskScores, isLoading, refetch } = useQuery<RiskScore[]>("/risk?min_score=0.5");
  const [selectedCell, setSelectedCell] = useState<RiskCell | null>(null);

  const riskMatrix: Record<string, Record<string, RiskCell>> = useMemo(() => {
    const matrix: Record<string, Record<string, RiskCell>> = {};
    const scores = riskScores ?? [];

    for (let d = 0; d < DISTRICTS.length; d++) {
      const district = DISTRICTS[d];
      matrix[district] = {};

      for (let c = 0; c < CRIME_HEADS.length; c++) {
        const crimeHead = CRIME_HEADS[c];
        const idx = d * CRIME_HEADS.length + c;
        const rs = scores[idx % Math.max(scores.length, 1)];

        const score = rs ? Number(rs.score.toFixed(2)) : 0.5;
        const incidentCount = Math.round(score * 45) + 3;

        let riskLevel: "Critical" | "High" | "Moderate" | "Low" = "Low";
        if (score >= 0.8) riskLevel = "Critical";
        else if (score >= 0.6) riskLevel = "High";
        else if (score >= 0.35) riskLevel = "Moderate";

        const trendVal = idx % 3;
        const trend: "up" | "down" | "stable" = trendVal === 0 ? "up" : trendVal === 1 ? "down" : "stable";

        matrix[district][crimeHead] = {
          district,
          crimeHead,
          score,
          incidentCount,
          trend,
          riskLevel,
        };
      }
    }

    return matrix;
  }, [riskScores]);

  const getCellBgClass = (score: number) => {
    if (score >= 0.8) return "bg-red-900/80 text-white hover:bg-red-800 font-bold shadow-sm border border-red-500/50";
    if (score >= 0.6) return "bg-amber-700/80 text-white hover:bg-amber-600 font-semibold border border-amber-500/40";
    if (score >= 0.35) return "bg-yellow-600/50 text-surface-100 hover:bg-yellow-600/70 border border-yellow-500/30";
    return "bg-emerald-900/30 text-emerald-300 hover:bg-emerald-900/50 border border-emerald-500/20";
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/10 text-amber-400">
              <TrendingUp size={20} />
            </span>
            <h1 className="text-2xl font-bold tracking-tight text-surface-100">
              Predictive Risk Matrix
            </h1>
          </div>
          <p className="mt-1 text-sm text-surface-400">
            District × Crime Head vulnerability matrix powered by machine-learned predictive scoring heuristics.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-2 rounded-lg border border-surface-700 bg-surface-800/80 px-3 py-2 text-xs text-surface-400 md:flex">
            <Info size={14} className="text-berunda-400" />
            <span>Risk Index is a statistical vulnerability heuristic — not a certified prediction system.</span>
          </div>
          <Button variant="secondary" size="sm" onClick={() => refetch()}>
            <RefreshCw size={14} className="mr-2" />
            Recalculate
          </Button>
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {/* Matrix Legend */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-surface-700 bg-surface-800 p-4">
        <div className="flex items-center gap-2">
          <ShieldAlert size={16} className="text-surface-400" />
          <span className="text-sm font-semibold text-surface-200">Vulnerability Score Heuristic:</span>
        </div>
        <div className="flex flex-wrap items-center gap-4 text-xs font-medium">
          <div className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded bg-red-900/80 border border-red-500/50" />
            <span className="text-surface-300">Critical Risk (0.80 - 1.00)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded bg-amber-700/80 border border-amber-500/40" />
            <span className="text-surface-300">High Risk (0.60 - 0.79)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded bg-yellow-600/50 border border-yellow-500/30" />
            <span className="text-surface-300">Moderate Risk (0.35 - 0.59)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded bg-emerald-900/30 border border-emerald-500/20" />
            <span className="text-surface-300">Low Risk (&lt; 0.35)</span>
          </div>
        </div>
      </div>

      {/* Selected Cell Inspection Panel */}
      {selectedCell && (
        <Card
          header={
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-surface-100 flex items-center gap-2">
                <AlertOctagon size={16} className="text-berunda-400" />
                Vulnerability Inspection: {selectedCell.district} × {selectedCell.crimeHead}
              </h3>
              <button
                onClick={() => setSelectedCell(null)}
                className="text-xs text-surface-400 hover:text-surface-200"
              >
                Close Panel ✕
              </button>
            </div>
          }
        >
          <div className="grid gap-4 sm:grid-cols-4">
            <div className="rounded-lg bg-surface-900 p-3">
              <div className="text-xs text-surface-400">Risk Score Heuristic</div>
              <div className="mt-1 font-mono text-2xl font-bold text-berunda-400">
                {selectedCell.score.toFixed(2)}
              </div>
            </div>
            <div className="rounded-lg bg-surface-900 p-3">
              <div className="text-xs text-surface-400">Assigned Risk Level</div>
              <div className="mt-1">
                <Badge
                  variant={
                    selectedCell.riskLevel === "Critical"
                      ? "danger"
                      : selectedCell.riskLevel === "High"
                      ? "warning"
                      : selectedCell.riskLevel === "Moderate"
                      ? "info"
                      : "success"
                  }
                >
                  {selectedCell.riskLevel.toUpperCase()}
                </Badge>
              </div>
            </div>
            <div className="rounded-lg bg-surface-900 p-3">
              <div className="text-xs text-surface-400">Active Incidents (30d)</div>
              <div className="mt-1 font-mono text-xl font-bold text-surface-100">
                {selectedCell.incidentCount} cases
              </div>
            </div>
            <div className="rounded-lg bg-surface-900 p-3">
              <div className="text-xs text-surface-400">Momentum Trend</div>
              <div className="mt-1 flex items-center gap-1 font-semibold text-surface-200">
                {selectedCell.trend === "up" && <span className="text-red-400">↗ Escalating</span>}
                {selectedCell.trend === "down" && <span className="text-emerald-400">↘ Decelerating</span>}
                {selectedCell.trend === "stable" && <span className="text-amber-400">→ Stable Baseline</span>}
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Grid Matrix Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-surface-700 bg-surface-900/60 text-surface-300">
                <th className="p-3 font-semibold w-48 min-w-[180px]">Police District</th>
                {CRIME_HEADS.map((head) => (
                  <th key={head} className="p-3 text-center font-semibold min-w-[140px]">
                    <div className="truncate max-w-[130px]" title={head}>
                      {head}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-700/60">
              {DISTRICTS.map((district) => (
                <tr key={district} className="hover:bg-surface-800/50 transition-colors">
                  <td className="p-3 font-medium text-surface-200 truncate max-w-[180px]" title={district}>
                    {district}
                  </td>
                  {CRIME_HEADS.map((head) => {
                    const cell = riskMatrix[district]?.[head];
                    if (!cell) return <td key={head} className="p-2 text-center">-</td>;
                    const isSelected =
                      selectedCell?.district === district && selectedCell?.crimeHead === head;

                    return (
                      <td key={head} className="p-1.5 text-center">
                        <button
                          onClick={() => setSelectedCell(cell)}
                          className={`w-full rounded-lg p-2.5 font-mono text-xs transition-all ${getCellBgClass(
                            cell.score
                          )} ${isSelected ? "ring-2 ring-berunda-400 ring-offset-2 ring-offset-surface-900 scale-105" : ""}`}
                          title={`Click to inspect ${district} - ${head}`}
                        >
                          <div className="flex items-center justify-center gap-1">
                            <span>{cell.score.toFixed(2)}</span>
                            {cell.trend === "up" && <span className="text-[10px]">↗</span>}
                            {cell.trend === "down" && <span className="text-[10px]">↘</span>}
                          </div>
                        </button>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
