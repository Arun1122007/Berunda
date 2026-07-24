import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { Shield, AlertCircle, Eye } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, demoLogin, isLoading, error } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as { from?: { pathname: string } })?.from
    ?.pathname || "/";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch {
      // Error is handled by useAuth
    }
  };

  const handleDemoLogin = async () => {
    try {
      await demoLogin();
      navigate(from, { replace: true });
    } catch {
      // Error is handled by useAuth
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-surface-900 px-4">
      <Card className="w-full max-w-md">
        <div className="mb-6 text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-berunda-600">
            <Shield className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-xl font-bold text-surface-100">
            Berunda
          </h1>
          <p className="mt-1 text-sm text-surface-400">
            Crime Intelligence Platform
          </p>
        </div>

        {error && (
          <div className="mb-4 flex items-center gap-2 rounded-lg bg-red-900/30 px-4 py-3 text-sm text-red-400">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="analyst@berunda.gov"
            required
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />
          <Button type="submit" className="w-full" isLoading={isLoading}>
            Sign In
          </Button>
          <Button
            type="button"
            variant="ghost"
            className="w-full"
            onClick={handleDemoLogin}
            isLoading={isLoading}
          >
            <Eye size={16} /> Demo Mode
          </Button>
        </form>
      </Card>
    </div>
  );
}
