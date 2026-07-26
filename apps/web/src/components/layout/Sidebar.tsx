import { NavLink, useNavigate } from "react-router-dom";
import clsx from "clsx";
import {
  LayoutDashboard,
  Map,
  Share2,
  BarChart3,
  MessageSquare,
  Shield,
  FileText,
  LogOut,
  Users,
  FolderOpen,
  AlertTriangle,
  TrendingUp,
  BarChart2,
  FileUp,
  FileSpreadsheet,
  UserSearch,
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const navSections = [
  {
    title: "Core Operations",
    items: [
      { to: "/", icon: LayoutDashboard, label: "Dashboard" },
      { to: "/cases", icon: FolderOpen, label: "FIR Cases" },
      { to: "/entities", icon: Users, label: "Entities" },
      { to: "/offenders", icon: UserSearch, label: "Offender Registry" },
      { to: "/hotspot", icon: Map, label: "Hotspot Map" },
      { to: "/graph", icon: Share2, label: "Link Graph" },
    ],
  },
  {
    title: "Intelligence & Analytics",
    items: [
      { to: "/analytics", icon: BarChart3, label: "Analytics Overview" },
      { to: "/anomalies", icon: AlertTriangle, label: "Statistical Anomalies" },
      { to: "/risk", icon: TrendingUp, label: "Risk Matrix" },
      { to: "/socioeconomic", icon: BarChart2, label: "Socioeconomic Drivers" },
      { to: "/ask-berunda", icon: MessageSquare, label: "Ask Berunda (RAG)" },
    ],
  },
  {
    title: "Governance & Ingestion",
    items: [
      { to: "/import", icon: FileUp, label: "Data Ingestion" },
      { to: "/reports", icon: FileSpreadsheet, label: "Automated Reports" },
      { to: "/admin", icon: Shield, label: "Admin Command" },
      { to: "/audit", icon: FileText, label: "Audit Ledger" },
    ],
  },
];

export default function Sidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <aside className="flex w-64 flex-col border-r border-surface-700 bg-surface-800">
      <div className="flex items-center gap-2 border-b border-surface-700 px-6 py-5">
        <Shield className="h-6 w-6 text-berunda-400" />
        <span className="text-lg font-bold tracking-tight text-surface-100">Berunda</span>
        <span className="ml-auto rounded bg-berunda-900 px-1.5 py-0.5 text-[10px] font-mono text-berunda-300 border border-berunda-700">
          INTEL
        </span>
      </div>

      <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-4 custom-scrollbar">
        {navSections.map((section) => (
          <div key={section.title} className="space-y-1">
            <h3 className="px-3 text-[11px] font-bold uppercase tracking-wider text-surface-500 font-mono">
              {section.title}
            </h3>
            <div className="mt-1 space-y-0.5">
              {section.items.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === "/"}
                  className={({ isActive }) =>
                    clsx(
                      "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all",
                      isActive
                        ? "bg-berunda-600/20 text-berunda-400 font-semibold shadow-sm border-l-2 border-berunda-500"
                        : "text-surface-400 hover:bg-surface-700/60 hover:text-surface-200"
                    )
                  }
                >
                  <item.icon size={17} className="shrink-0" />
                  <span className="truncate">{item.label}</span>
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </nav>
      
      <div className="border-t border-surface-700 p-3">
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-surface-400 hover:bg-surface-700/80 hover:text-red-400 transition-colors"
        >
          <LogOut size={17} />
          Logout Session
        </button>
      </div>
    </aside>
  );
}
