import { Search, Bell, User } from "lucide-react";
import { useState } from "react";
import Input from "@/components/ui/Input";
import { useAuth } from "@/hooks/useAuth";
import Badge from "@/components/ui/Badge";

export default function Header() {
  const [searchQuery, setSearchQuery] = useState("");
  const { user } = useAuth();

  return (
    <header className="flex h-16 items-center justify-between border-b border-surface-700 bg-surface-800 px-6">
      <div className="w-96">
        <Input
          placeholder="Search cases, persons, FIR numbers..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          icon={<Search size={16} />}
        />
      </div>

      <div className="flex items-center gap-4">
        <button className="relative rounded-lg p-2 text-surface-400 hover:bg-surface-700 hover:text-surface-200 transition-colors" aria-label="Notifications">
          <Bell size={20} />
          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500" />
        </button>

        <div className="flex items-center gap-3 rounded-lg border border-surface-700 px-3 py-2 bg-surface-800/50 hover:border-surface-600 transition-colors">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-berunda-600">
            <User size={16} className="text-white" />
          </div>
          <div className="text-sm">
            <div className="flex items-center gap-2">
              <p className="font-medium text-surface-200">{user?.name || "Analyst User"}</p>
              {user?.role && (
                <Badge variant="info" className="uppercase text-[10px] px-1.5 py-0">
                  {user.role}
                </Badge>
              )}
            </div>
            <p className="text-xs text-surface-400">{user?.email || "analyst@berunda.gov"}</p>
          </div>
        </div>
      </div>
    </header>
  );
}
