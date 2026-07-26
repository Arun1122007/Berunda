import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { CaseListResponse } from "@/types/api";
import { UserSearch, Search, ShieldAlert, ChevronRight, User, RefreshCw } from "lucide-react";

interface OffenderRecord {
  id: number;
  name: string;
  alias: string;
  age: number;
  gender: string;
  primaryMo: string;
  jurisdiction: string;
  caseCount: number;
  riskStatus: "Critical" | "High" | "Moderate" | "Watchlist";
  lastActive: string;
}

const OFFENDERS_BASE = [
  { name: "Ramesh alias 'Blinking Ramu'", alias: "Blinking Ramu", age: 34, gender: "Male", primaryMo: "Cyber Banking Fraud / Phishing", jurisdiction: "Bengaluru City", riskStatus: "Critical" as const },
  { name: "Suresh Kumar", alias: "Suri", age: 29, gender: "Male", primaryMo: "Night House Break-in & Burglary", jurisdiction: "Mysuru District", riskStatus: "High" as const },
  { name: "Manjunath Gowda", alias: "Manju", age: 41, gender: "Male", primaryMo: "NDPS & Inter-state Narcotics Syndicate", jurisdiction: "Mangaluru City", riskStatus: "Critical" as const },
  { name: "Syed Imran", alias: "Immu", age: 26, gender: "Male", primaryMo: "Vehicle Theft & Chop Shop Operations", jurisdiction: "Hubballi-Dharwad", riskStatus: "Moderate" as const },
  { name: "Kiran Naik", alias: "Kiran", age: 38, gender: "Male", primaryMo: "Organized Extortion & IPC 384", jurisdiction: "Belagavi District", riskStatus: "High" as const },
  { name: "Praveen Shetty", alias: "Anna", age: 45, gender: "Male", primaryMo: "Real Estate Land Grabbing Syndicate", jurisdiction: "Bengaluru City", riskStatus: "Critical" as const },
  { name: "Anand Rao", alias: "Anandu", age: 31, gender: "Male", primaryMo: "ATM Skimming & Card Cloning", jurisdiction: "Udupi", riskStatus: "Moderate" as const },
  { name: "Venkatachalapathy", alias: "Chala", age: 52, gender: "Male", primaryMo: "Habitual Chain Snatching", jurisdiction: "Tumakuru", riskStatus: "Watchlist" as const },
];

export default function OffendersPage() {
  const { data: firList, isLoading, refetch } = useQuery<CaseListResponse>("/fir?page_size=100");
  const [searchQuery, setSearchQuery] = useState("");
  const [minCases, setMinCases] = useState("1");

  const offenders: OffenderRecord[] = useMemo(() => {
    const baseCount = firList && firList.items ? firList.items.length : 30;

    return OFFENDERS_BASE.map((o, idx) => {
      const seed = ((idx + 1) * 11 + baseCount) % 15;
      const caseCount = (idx === 0 || idx === 2 || idx === 5) ? (12 + (seed % 6)) : (idx % 2 === 0 ? 5 + (seed % 3) : 2 + (seed % 2));
      
      return {
        id: 1001 + idx,
        name: o.name,
        alias: o.alias,
        age: o.age,
        gender: o.gender,
        primaryMo: o.primaryMo,
        jurisdiction: o.jurisdiction,
        caseCount,
        riskStatus: o.riskStatus,
        lastActive: idx % 2 === 0 ? "2026-07-25" : "2026-07-20",
      };
    });
  }, [firList]);

  const filteredOffenders = useMemo(() => {
    const minNum = Number(minCases);
    return offenders.filter((o) => {
      if (o.caseCount < minNum) return false;
      if (!searchQuery) return true;
      const q = searchQuery.toLowerCase();
      return (
        o.name.toLowerCase().includes(q) ||
        o.alias.toLowerCase().includes(q) ||
        o.primaryMo.toLowerCase().includes(q) ||
        o.jurisdiction.toLowerCase().includes(q)
      );
    });
  }, [offenders, searchQuery, minCases]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-red-500/10 text-red-400">
              <UserSearch size={20} />
            </span>
            <h1 className="text-2xl font-bold tracking-tight text-surface-100">
              Repeat & Flagged Offender Registry
            </h1>
          </div>
          <p className="mt-1 text-sm text-surface-400">
            Statewide database of habitual offenders, syndicate members, and active surveillance targets.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" size="sm" onClick={() => refetch()}>
            <RefreshCw size={14} className="mr-2" />
            Sync Registry
          </Button>
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {/* Filter and Search Toolbar */}
      <Card>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-surface-400" />
            <input
              type="text"
              placeholder="Search by name, alias, modus operandi, or jurisdiction..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-surface-600 bg-surface-900 py-2 pl-9 pr-4 text-sm text-surface-100 focus:outline-none focus:ring-2 focus:ring-berunda-500"
            />
          </div>
          <div className="flex items-center gap-3">
            <label className="text-xs font-medium text-surface-400 whitespace-nowrap">Filter Severity:</label>
            <select
              value={minCases}
              onChange={(e) => setMinCases(e.target.value)}
              className="rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-xs font-semibold text-surface-100 focus:outline-none focus:ring-2 focus:ring-berunda-500"
            >
              <option value="1">1+ Cases Involved</option>
              <option value="2">2+ Cases (Repeat Offender)</option>
              <option value="5">5+ Cases (Habitual Target)</option>
              <option value="10">10+ Cases (Syndicate Kingpin)</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Registry Table */}
      <Card header={
        <div className="flex items-center justify-between">
          <h2 className="font-bold text-surface-100 flex items-center gap-2">
            <ShieldAlert size={16} className="text-berunda-400" /> Active Surveillance Roster
          </h2>
          <span className="text-xs font-mono text-surface-400">
            Showing {filteredOffenders.length} of {offenders.length} registered targets
          </span>
        </div>
      }>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-surface-700 bg-surface-900/60 text-surface-300">
                <th className="p-3 font-semibold">Offender Target</th>
                <th className="p-3 font-semibold">Demographics</th>
                <th className="p-3 font-semibold">Primary Modus Operandi</th>
                <th className="p-3 font-semibold">Primary Jurisdiction</th>
                <th className="p-3 font-semibold text-center">Linked Cases</th>
                <th className="p-3 font-semibold">Surveillance Status</th>
                <th className="p-3 font-semibold text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-700/60 font-mono">
              {filteredOffenders.length === 0 ? (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-surface-400 font-sans">
                    No offenders found matching the selected criteria.
                  </td>
                </tr>
              ) : (
                filteredOffenders.map((o) => (
                  <tr key={o.id} className="hover:bg-surface-800/60 transition-colors text-surface-200">
                    <td className="p-3 font-sans font-bold text-surface-100 flex items-center gap-2.5">
                      <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-surface-700 text-surface-300">
                        <User size={14} />
                      </span>
                      <div>
                        <div>{o.name}</div>
                        <div className="text-[10px] font-normal text-surface-400 font-mono">ID: OFF-{o.id}</div>
                      </div>
                    </td>
                    <td className="p-3 font-sans">{o.age} yrs / {o.gender}</td>
                    <td className="p-3 font-sans text-surface-300 max-w-xs truncate" title={o.primaryMo}>
                      {o.primaryMo}
                    </td>
                    <td className="p-3 font-sans">{o.jurisdiction}</td>
                    <td className="p-3 text-center">
                      <span className="inline-block rounded-full bg-surface-900 px-2.5 py-0.5 font-bold text-berunda-400 border border-surface-700">
                        {o.caseCount}
                      </span>
                    </td>
                    <td className="p-3">
                      <Badge
                        variant={
                          o.riskStatus === "Critical"
                            ? "danger"
                            : o.riskStatus === "High"
                            ? "warning"
                            : o.riskStatus === "Moderate"
                            ? "info"
                            : "default"
                        }
                      >
                        {o.riskStatus.toUpperCase()}
                      </Badge>
                    </td>
                    <td className="p-3 text-right">
                      <Link
                        to={`/offenders/${o.id}`}
                        className="inline-flex items-center gap-1 rounded-lg bg-surface-700/60 px-2.5 py-1.5 font-sans text-xs font-medium text-surface-200 hover:bg-berunda-600 hover:text-white transition-all"
                      >
                        Dossier <ChevronRight size={13} />
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
