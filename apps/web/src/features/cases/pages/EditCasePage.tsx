import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery, useMutation } from "@/hooks/useApi";
import { ArrowLeft, AlertCircle, CheckCircle } from "lucide-react";
import type { Case, CaseDetail } from "@/types/api";

interface FormErrors {
  [key: string]: string;
}

export default function EditCasePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: existing, isLoading: loadingExisting, error: loadError } = useQuery<CaseDetail>(
    `/fir/${id}`, { enabled: !!id }
  );

  const { isLoading: isSubmitting, error: submitError, mutate } = useMutation<Case>(
    `/fir/${id}`, "PUT"
  );

  const [formData, setFormData] = useState({
    crimeNo: "",
    caseNo: "",
    crimeRegisteredDate: "",
    policeStationId: "",
    caseCategoryId: "1",
    gravityOffenceId: "2",
    crimeMajorHeadId: "",
    crimeMinorHeadId: "",
    caseStatusId: "1",
    incidentFromDate: "",
    incidentToDate: "",
    briefFacts: "",
    latitude: "",
    longitude: "",
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (existing) {
      setFormData({
        crimeNo: existing.crimeNo || "",
        caseNo: existing.caseNo || "",
        crimeRegisteredDate: existing.crimeRegisteredDate || "",
        policeStationId: existing.policeStationId?.toString() || "",
        caseCategoryId: "1",
        gravityOffenceId: "2",
        crimeMajorHeadId: existing.crimeMajorHeadId?.toString() || "",
        crimeMinorHeadId: existing.crimeMinorHeadId?.toString() || "",
        caseStatusId: existing.caseStatusId?.toString() || "1",
        incidentFromDate: existing.incidentFromDate || "",
        incidentToDate: existing.incidentToDate || "",
        briefFacts: existing.briefFacts || "",
        latitude: existing.latitude?.toString() || "",
        longitude: existing.longitude?.toString() || "",
      });
    }
  }, [existing]);

  const validate = (): boolean => {
    const errs: FormErrors = {};
    if (!formData.crimeNo.trim()) {
      errs.crimeNo = "Crime No is required";
    }
    if (formData.briefFacts.length > 5000) {
      errs.briefFacts = "Brief facts must be under 5000 characters";
    }
    if (formData.latitude && !formData.longitude) {
      errs.longitude = "Longitude is required when latitude is provided";
    }
    if (formData.longitude && !formData.latitude) {
      errs.latitude = "Latitude is required when longitude is provided";
    }
    if (formData.latitude) {
      const lat = parseFloat(formData.latitude);
      if (isNaN(lat) || lat < -90 || lat > 90) {
        errs.latitude = "Latitude must be between -90 and 90";
      }
    }
    if (formData.longitude) {
      const lng = parseFloat(formData.longitude);
      if (isNaN(lng) || lng < -180 || lng > 180) {
        errs.longitude = "Longitude must be between -180 and 180";
      }
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    const body: Record<string, unknown> = {
      crimeNo: formData.crimeNo,
    };
    if (formData.caseNo) body.caseNo = formData.caseNo;
    if (formData.crimeRegisteredDate) body.crimeRegisteredDate = formData.crimeRegisteredDate;
    if (formData.policeStationId) body.policeStationId = parseInt(formData.policeStationId);
    if (formData.crimeMajorHeadId) body.crimeMajorHeadId = parseInt(formData.crimeMajorHeadId);
    if (formData.crimeMinorHeadId) body.crimeMinorHeadId = parseInt(formData.crimeMinorHeadId);
    if (formData.caseCategoryId) body.caseCategoryId = parseInt(formData.caseCategoryId);
    if (formData.gravityOffenceId) body.gravityOffenceId = parseInt(formData.gravityOffenceId);
    if (formData.caseStatusId) body.caseStatusId = parseInt(formData.caseStatusId);
    if (formData.incidentFromDate) body.incidentFromDate = formData.incidentFromDate;
    if (formData.incidentToDate) body.incidentToDate = formData.incidentToDate;
    if (formData.briefFacts) body.briefFacts = formData.briefFacts;
    if (formData.latitude) body.latitude = parseFloat(formData.latitude);
    if (formData.longitude) body.longitude = parseFloat(formData.longitude);

    const result = await mutate(body);
    if (result) {
      setSuccess(true);
      setTimeout(() => {
        navigate(`/cases/${id}`);
      }, 1500);
    }
  };

  if (loadingExisting) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-20">
        <div className="flex items-center gap-2 text-red-400">
          <AlertCircle size={20} />
          <p className="text-sm">{loadError}</p>
        </div>
        <Button variant="secondary" onClick={() => navigate("/cases")}>
          <ArrowLeft size={16} /> Back to Cases
        </Button>
      </div>
    );
  }

  if (success) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-20">
        <CheckCircle size={48} className="text-green-400" />
        <p className="text-lg font-medium text-surface-100">Case updated successfully!</p>
        <p className="text-sm text-surface-400">Redirecting to case detail...</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate(`/cases/${id}`)}>
          <ArrowLeft size={16} /> Back
        </Button>
        <h1 className="text-2xl font-bold tracking-tight text-surface-100">
          Edit Case {id}
        </h1>
      </div>

      {submitError && (
        <div className="flex items-center gap-2 rounded-lg bg-red-900/30 px-4 py-3 text-sm text-red-400">
          <AlertCircle size={16} />
          {submitError}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card header={<h2 className="font-semibold text-surface-100">Required Information</h2>}>
          <div className="space-y-4">
            <Input
              label="Crime No *"
              value={formData.crimeNo}
              onChange={(e) => handleChange("crimeNo", e.target.value)}
              placeholder="CR-2026-0001"
              error={errors.crimeNo}
              required
            />
          </div>
        </Card>

        <Card header={<h2 className="font-semibold text-surface-100">Case Details</h2>}>
          <div className="grid gap-4 sm:grid-cols-2">
            <Input
              label="Case No"
              value={formData.caseNo}
              onChange={(e) => handleChange("caseNo", e.target.value)}
              placeholder="42/2026"
            />
            <Input
              label="Registered Date"
              type="date"
              value={formData.crimeRegisteredDate}
              onChange={(e) => handleChange("crimeRegisteredDate", e.target.value)}
            />
            <Input
              label="Police Station ID"
              type="number"
              value={formData.policeStationId}
              onChange={(e) => handleChange("policeStationId", e.target.value)}
              placeholder="5"
            />
            <Input
              label="Case Category ID"
              type="number"
              value={formData.caseCategoryId}
              onChange={(e) => handleChange("caseCategoryId", e.target.value)}
            />
            <Input
              label="Gravity Offence ID"
              type="number"
              value={formData.gravityOffenceId}
              onChange={(e) => handleChange("gravityOffenceId", e.target.value)}
            />
            <Input
              label="Crime Major Head ID"
              type="number"
              value={formData.crimeMajorHeadId}
              onChange={(e) => handleChange("crimeMajorHeadId", e.target.value)}
              placeholder="1"
            />
            <Input
              label="Crime Minor Head ID"
              type="number"
              value={formData.crimeMinorHeadId}
              onChange={(e) => handleChange("crimeMinorHeadId", e.target.value)}
            />
            <Input
              label="Case Status ID"
              type="number"
              value={formData.caseStatusId}
              onChange={(e) => handleChange("caseStatusId", e.target.value)}
            />
          </div>
        </Card>

        <Card header={<h2 className="font-semibold text-surface-100">Incident Details</h2>}>
          <div className="grid gap-4 sm:grid-cols-2">
            <Input
              label="Incident From"
              type="datetime-local"
              value={formData.incidentFromDate}
              onChange={(e) => handleChange("incidentFromDate", e.target.value)}
            />
            <Input
              label="Incident To"
              type="datetime-local"
              value={formData.incidentToDate}
              onChange={(e) => handleChange("incidentToDate", e.target.value)}
            />
            <Input
              label="Latitude"
              type="number"
              step="any"
              value={formData.latitude}
              onChange={(e) => handleChange("latitude", e.target.value)}
              placeholder="12.9716"
              error={errors.latitude}
            />
            <Input
              label="Longitude"
              type="number"
              step="any"
              value={formData.longitude}
              onChange={(e) => handleChange("longitude", e.target.value)}
              placeholder="77.5946"
              error={errors.longitude}
            />
          </div>
        </Card>

        <Card header={<h2 className="font-semibold text-surface-100">Brief Facts</h2>}>
          <div>
            <textarea
              className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 placeholder-surface-500 transition-colors focus:outline-none focus:ring-2 focus:ring-berunda-500 hover:border-surface-500"
              rows={5}
              value={formData.briefFacts}
              onChange={(e) => handleChange("briefFacts", e.target.value)}
              placeholder="Describe the incident..."
            />
            {errors.briefFacts && (
              <p className="mt-1 text-sm text-red-400">{errors.briefFacts}</p>
            )}
          </div>
        </Card>

        <div className="flex justify-end gap-3">
          <Button variant="secondary" onClick={() => navigate(`/cases/${id}`)}>
            Cancel
          </Button>
          <Button type="submit" isLoading={isSubmitting}>
            {isSubmitting ? "Saving..." : "Save Changes"}
          </Button>
        </div>
      </form>
    </div>
  );
}
