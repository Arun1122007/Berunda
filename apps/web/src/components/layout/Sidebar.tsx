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
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const navItems = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/cases", icon: FolderOpen, label: "FIR Cases" },
  { to: "/hotspot", icon: Map, label: "Hotspot Map" },
  { to: "/graph", icon: Share2, label: "Link Graph" },
  { to: "/entities", icon: Users, label: "Entities" },
  { to: "/analytics", icon: BarChart3, label: "Analytics" },
  { to: "/ask-berunda", icon: MessageSquare, label: "Ask Berunda" },
  { to: "/admin", icon: Shield, label: "Admin" },
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
        <span className="text-lg font-bold text-surface-100">Berunda</span>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-4">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              clsx(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-berunda-600/20 text-berunda-400"
                  : "text-surface-400 hover:bg-surface-700 hover:text-surface-200"
              )
            }
          >
            <item.icon size={18} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-surface-700 px-3 py-4 space-y-1">
        <NavLink
          to="/audit"
          className={({ isActive }) =>
            clsx(
              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors w-full",
              isActive
                ? "bg-berunda-600/20 text-berunda-400"
                : "text-surface-400 hover:bg-surface-700 hover:text-surface-200"
            )
          }
        >
          <FileText size={18} />
          Audit Log
        </NavLink>
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-surface-400 hover:bg-surface-700 hover:text-red-400 transition-colors"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </aside>
  );
}
