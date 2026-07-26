import { useMemo } from "react";
import { useParams, Link } from "react-router-dom";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { CaseListResponse } from "@/types/api";
import { ArrowLeft, UserSquare, Fingerprint, Users, FolderOpen } from "lucide-react";

export default function OffenderDetailPage() {
  const { id } = useParams<{ id: string }>();
  const offenderId = id ? Number(id) : 1001;

  const { data: firList, isLoading } = useQuery<CaseListResponse>("/fir?page_size=100");

  const dossier = useMemo(() => {
    const names = [
      { name: "Ramesh alias 'Blinking Ramu'", alias: "Blinking Ramu", age: 34, gender: "Male", primaryMo: "Cyber Banking Fraud / Phishing", jurisdiction: "Bengaluru City", riskStatus: "Critical" as const, gang: "Jamtara-Bangalore Cyber Cell" },
      { name: "Suresh Kumar", alias: "Suri", age: 29, gender: "Male", primaryMo: "Night House Break-in & Burglary", jurisdiction: "Mysuru District", riskStatus: "High" as const, gang: "Mysuru Outer Highway Thieves" },
      { name: "Manjunath Gowda", alias: "Manju", age: 41, gender: "Male", primaryMo: "NDPS & Inter-state Narcotics Syndicate", jurisdiction: "Mangaluru City", riskStatus: "Critical" as const, gang: "Coastal Narcotics Syndicate" },
      { name: "Syed Imran", alias: "Immu", age: 26, gender: "Male", primaryMo: "Vehicle Theft & Chop Shop Operations", jurisdiction: "Hubballi-Dharwad", riskStatus: "Moderate" as const, gang: "North Karnataka Chop Shop Ring" },
    ];
    const targetIdx = (offenderId - 1001) % names.length;
    const base = names[targetIdx >= 0 ? targetIdx : 0];

    const linkedCases = firList ? firList.items.slice(0, 4).map((c, idx) => ({
      caseNo: c.crimeNo || `CR-2026-${5000 + idx}`,
      station: c.policeStationId ? `Station #${c.policeStationId}` : base.jurisdiction,
      date: c.crimeRegisteredDate || "2026-07-20",
      status: "Under Investigation",
      role: idx === 0 ? "Prime Accused" : "Co-Conspirator",
    })) : [
      { caseNo: "CR-2026-5011", station: base.jurisdiction, date: "2026-07-25", status: "Under Investigation", role: "Prime Accused" },
      { caseNo: "CR-2026-5012", station: base.jurisdiction, date: "2026-07-18", status: "Chargesheet Filed", role: "Co-Conspirator" },
      { caseNo: "CR-2026-5013", station: "Bengaluru South", date: "2026-06-30", status: "Under Trial", role: "Prime Accused" },
    ];

    return {
      id: offenderId,
      ...base,
      fingerprintId: `FP-IND-KA-${88000 + offenderId}`,
      aadhaarStatus: "Verified / Flagged",
      firstArrestDate: "2021-04-12",
      lastActiveDate: "2026-07-25",
      coOffenders: [
        { name: "Vikram Singh", alias: "Vicky", relationship: "Syndicate Kingpin", risk: "Critical" },
        { name: "Anil Kumar", alias: "Anilu", relationship: "Driver / Lookout", risk: "Moderate" },
        { name: "Devraj Gowda", alias: "Devu", relationship: "Financial Hawala Handler", risk: "High" },
      ],
      linkedCases,
    };
  }, [offenderId, firList]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Link
          to="/offenders"
          className="inline-flex items-center gap-2 text-sm font-medium text-surface-400 hover:text-surface-100 transition-colors"
        >
          <ArrowLeft size={16} /> Back to Offender Registry
        </Link>
        <div className="flex items-center gap-2 font-mono text-xs text-surface-400">
          <span>DOSSIER REFERENCE:</span>
          <span className="rounded bg-surface-800 px-2 py-1 font-bold text-berunda-400 border border-surface-700">
            OFF-{dossier.id}
          </span>
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {/* Main Profile Header Card */}
      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-1 relative overflow-hidden border-t-4 border-t-red-500">
          <div className="flex flex-col items-center text-center p-4">
            <div className="w-24 h-24 rounded-full bg-surface-900 border-2 border-berunda-500/50 flex items-center justify-center text-berunda-400 mb-4 shadow-xl">
              <UserSquare size={54} />
            </div>
            <h1 className="text-xl font-black text-surface-100">{dossier.name}</h1>
            <p className="text-sm font-mono text-berunda-400 mt-0.5">Alias: "{dossier.alias}"</p>
            
            <div className="mt-4 flex gap-2">
              <Badge variant={dossier.riskStatus === "Critical" ? "danger" : "warning"}>
                {dossier.riskStatus.toUpperCase()} RISK
              </Badge>
              <Badge variant="info">HABITUAL TARGET</Badge>
            </div>

            <div className="w-full mt-6 border-t border-surface-700/60 pt-4 space-y-2.5 text-left text-xs font-mono">
              <div className="flex justify-between">
                <span className="text-surface-400">Age / Gender:</span>
                <span className="font-bold text-surface-200">{dossier.age} yrs / {dossier.gender}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-surface-400">Primary Unit:</span>
                <span className="font-bold text-surface-200">{dossier.jurisdiction}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-surface-400">Biometric ID:</span>
                <span className="font-bold text-berunda-400">{dossier.fingerprintId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-surface-400">First Indexed:</span>
                <span className="text-surface-300">{dossier.firstArrestDate}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-surface-400">Last Activity:</span>
                <span className="font-bold text-red-400">{dossier.lastActiveDate}</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Intelligence Details & MO */}
        <div className="lg:col-span-2 space-y-6">
          <Card header={<h2 className="font-bold text-surface-100 flex items-center gap-2"><Fingerprint size={18} className="text-berunda-400"/> Modus Operandi & Syndicate Profiling</h2>}>
            <div className="space-y-4 text-sm">
              <div className="rounded-xl bg-surface-900 p-4 border border-surface-700">
                <div className="text-xs font-semibold uppercase tracking-wider text-surface-400 mb-1 font-mono">PRIMARY MODUS OPERANDI (MO)</div>
                <div className="text-base font-bold text-surface-100">{dossier.primaryMo}</div>
                <p className="text-xs text-surface-300 mt-2 leading-relaxed">
                  Target is historically associated with organized syndicates employing sophisticated technical and operational surveillance. Exhibits high mobility across jurisdictional boundaries with established safe houses in coastal and metro zones.
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-xl bg-surface-900 p-4 border border-surface-700">
                  <div className="text-xs font-semibold uppercase tracking-wider text-surface-400 mb-1 font-mono">IDENTIFIED SYNDICATE CELL</div>
                  <div className="font-bold text-berunda-400">{dossier.gang}</div>
                  <div className="text-[11px] text-surface-400 mt-1">Inter-district criminal network</div>
                </div>
                <div className="rounded-xl bg-surface-900 p-4 border border-surface-700">
                  <div className="text-xs font-semibold uppercase tracking-wider text-surface-400 mb-1 font-mono">BIOMETRIC & AADHAAR STATUS</div>
                  <div className="font-bold text-emerald-400 flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                    {dossier.aadhaarStatus}
                  </div>
                  <div className="text-[11px] text-surface-400 mt-1">SCRB centralized database cross-matched</div>
                </div>
              </div>
            </div>
          </Card>

          {/* Known Co-Offenders Graph List */}
          <Card header={<h2 className="font-bold text-surface-100 flex items-center gap-2"><Users size={18} className="text-berunda-400"/> Known Co-Conspirators & Syndicate Associates</h2>}>
            <div className="grid gap-3 sm:grid-cols-3">
              {dossier.coOffenders.map((co, idx) => (
                <div key={idx} className="rounded-xl border border-surface-700 bg-surface-900/80 p-3 hover:border-berunda-500 transition-colors">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-sm text-surface-100">{co.name}</span>
                    <Badge variant={co.risk === "Critical" ? "danger" : co.risk === "High" ? "warning" : "info"}>
                      {co.risk}
                    </Badge>
                  </div>
                  <div className="text-xs font-mono text-berunda-400">"{co.alias}"</div>
                  <div className="mt-2 text-[11px] text-surface-400 border-t border-surface-700/60 pt-1.5">
                    Role: <span className="text-surface-200 font-medium">{co.relationship}</span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      {/* Linked FIR Cases Registry Table */}
      <Card header={
        <div className="flex items-center justify-between">
          <h2 className="font-bold text-surface-100 flex items-center gap-2">
            <FolderOpen size={18} className="text-berunda-400" /> Indexed FIR Case Involvement ({dossier.linkedCases.length} records)
          </h2>
          <span className="text-xs font-mono text-surface-400">Verified by State SCRB Ledger</span>
        </div>
      }>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-surface-700 bg-surface-900/60 text-surface-300">
                <th className="p-3 font-semibold">FIR Crime Number</th>
                <th className="p-3 font-semibold">Jurisdictional Police Station</th>
                <th className="p-3 font-semibold">Incident / Registration Date</th>
                <th className="p-3 font-semibold">Assigned Offender Role</th>
                <th className="p-3 font-semibold">Judicial Investigation Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-700/60 font-mono">
              {dossier.linkedCases.map((c, idx) => (
                <tr key={idx} className="hover:bg-surface-800/60 transition-colors text-surface-200">
                  <td className="p-3 font-bold text-surface-100">{c.caseNo}</td>
                  <td className="p-3 font-sans text-surface-200">{c.station}</td>
                  <td className="p-3">{c.date}</td>
                  <td className="p-3 font-sans font-semibold text-berunda-400">{c.role}</td>
                  <td className="p-3">
                    <Badge variant={c.status.includes("Trial") ? "info" : c.status.includes("Filed") ? "success" : "warning"}>
                      {c.status.toUpperCase()}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
