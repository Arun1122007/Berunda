import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { Settings, Users, Database, RefreshCw } from "lucide-react";

export default function AdminPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Admin</h1>
        <p className="mt-1 text-sm text-surface-400">
          System configuration and user management
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <div className="flex items-center gap-3">
            <Users className="h-8 w-8 text-berunda-400" />
            <div>
              <h3 className="font-medium text-surface-200">User Management</h3>
              <p className="text-xs text-surface-400">Manage analysts and roles</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-3">
            <Database className="h-8 w-8 text-berunda-400" />
            <div>
              <h3 className="font-medium text-surface-200">Data Sources</h3>
              <p className="text-xs text-surface-400">Configure import pipelines</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-3">
            <RefreshCw className="h-8 w-8 text-berunda-400" />
            <div>
              <h3 className="font-medium text-surface-200">Scheduled Jobs</h3>
              <p className="text-xs text-surface-400">Cron job management</p>
            </div>
          </div>
        </Card>
      </div>

      <Card className="p-0">
        <div className="border-b border-surface-700 px-6 py-4">
          <h2 className="font-semibold text-surface-100">System Settings</h2>
        </div>
        <div className="p-6">
          <p className="text-sm text-surface-400">
            Admin settings panel — configure system parameters, manage user
            access, and monitor data pipeline health.
          </p>
        </div>
      </Card>
    </div>
  );
}
