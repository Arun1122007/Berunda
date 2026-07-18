import { Search, Bell, User } from "lucide-react";
import { useState } from "react";
import Input from "@/components/ui/Input";

export default function Header() {
  const [searchQuery, setSearchQuery] = useState("");

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
        <button className="relative rounded-lg p-2 text-surface-400 hover:bg-surface-700 hover:text-surface-200 transition-colors">
          <Bell size={20} />
          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500" />
        </button>

        <div className="flex items-center gap-3 rounded-lg border border-surface-700 px-3 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-berunda-600">
            <User size={16} className="text-white" />
          </div>
          <div className="text-sm">
            <p className="font-medium text-surface-200">Analyst User</p>
            <p className="text-xs text-surface-400">analyst@berunda.gov</p>
          </div>
        </div>
      </div>
    </header>
  );
}
