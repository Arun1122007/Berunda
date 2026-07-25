import { useNavigate } from "react-router-dom";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { AlertTriangle, ArrowLeft, Home } from "lucide-react";

export default function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-[70vh] items-center justify-center p-4">
      <Card className="max-w-md w-full text-center py-12 px-6">
        <div className="flex justify-center mb-6">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-900/30 text-red-400">
            <AlertTriangle size={36} />
          </div>
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-surface-100 mb-2">
          404 — Page Not Found
        </h1>
        <p className="text-sm text-surface-400 mb-8 leading-relaxed">
          The page or resource you are looking for does not exist, has been removed, or you do not have permission to view it.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <Button variant="secondary" onClick={() => navigate(-1)} className="w-full sm:w-auto">
            <ArrowLeft size={16} /> Go Back
          </Button>
          <Button onClick={() => navigate("/")} className="w-full sm:w-auto">
            <Home size={16} /> Dashboard
          </Button>
        </div>
      </Card>
    </div>
  );
}
