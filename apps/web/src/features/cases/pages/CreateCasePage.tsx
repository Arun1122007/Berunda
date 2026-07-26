import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { useMutation } from "@/hooks/useApi";
import { ArrowLeft, AlertCircle, CheckCircle } from "lucide-react";
import type { Case } from "@/types/api";

interface FormErrors {
  [key: string]: string;
}

export default function CreateCasePage() {
  const navigate = useNavigate();
  const { isLoading: isSubmitting, error: submitError, mutate } = useMutation<Case>(
    "/fir",
    "POST"
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

  const [persons, setPersons] = useState<Array<{ name: string; type: "Complainant" | "Victim" | "Accused"; age: string }>>([]);
  const [vehicles, setVehicles] = useState<Array<{ regNo: string; make: string }>>([]);

  const [errors, setErrors] = useState<FormErrors>({});
  const [success, setSuccess] = useState(false);

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
    if (persons.length > 0) body.persons = persons;
    if (vehicles.length > 0) body.vehicles = vehicles;

    const result = await mutate(body);
    if (result) {
      setSuccess(true);
      setTimeout(() => {
        navigate(`/cases/${result.caseMasterId}`);
      }, 1500);
    }
  };

  if (success) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-20">
        <CheckCircle size={48} className="text-green-400" />
        <p className="text-lg font-medium text-surface-100">Case created successfully!</p>
        <p className="text-sm text-surface-400">Redirecting to case detail...</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate("/cases")}>
          <ArrowLeft size={16} /> Back
        </Button>
        <h1 className="text-2xl font-bold tracking-tight text-surface-100">
          Create New Case
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

        <Card header={<h2 className="font-semibold text-surface-100">Associated Persons (Complainants, Victims, Accused)</h2>}>
          <div className="space-y-4">
            {persons.map((p, idx) => (
              <div key={idx} className="flex items-center justify-between rounded-lg bg-surface-800 p-3 text-sm text-surface-200">
                <span>{p.name} ({p.type}, Age: {p.age || "N/A"})</span>
                <button type="button" onClick={() => setPersons(persons.filter((_, i) => i !== idx))} className="text-red-400 hover:text-red-300">Remove</button>
              </div>
            ))}
            <div className="flex flex-wrap items-end gap-3">
              <Input label="Name" id="new-person-name" placeholder="Ramesh Kumar" className="flex-1" />
              <div className="w-40">
                <label className="block text-xs font-medium text-surface-400 mb-1">Type</label>
                <select id="new-person-type" className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 focus:outline-none focus:ring-2 focus:ring-berunda-500">
                  <option value="Accused">Accused</option>
                  <option value="Victim">Victim</option>
                  <option value="Complainant">Complainant</option>
                </select>
              </div>
              <Input label="Age" id="new-person-age" type="number" placeholder="30" className="w-24" />
              <Button type="button" variant="secondary" onClick={() => {
                const nameEl = document.getElementById("new-person-name") as HTMLInputElement;
                const typeEl = document.getElementById("new-person-type") as HTMLSelectElement;
                const ageEl = document.getElementById("new-person-age") as HTMLInputElement;
                if (nameEl && nameEl.value.trim()) {
                  setPersons([...persons, { name: nameEl.value.trim(), type: typeEl.value as "Complainant" | "Victim" | "Accused", age: ageEl.value }]);
                  nameEl.value = "";
                  ageEl.value = "";
                }
              }}>+ Add Person</Button>
            </div>
          </div>
        </Card>

        <Card header={<h2 className="font-semibold text-surface-100">Associated Vehicles</h2>}>
          <div className="space-y-4">
            {vehicles.map((v, idx) => (
              <div key={idx} className="flex items-center justify-between rounded-lg bg-surface-800 p-3 text-sm text-surface-200">
                <span>{v.regNo} ({v.make || "Unknown Make"})</span>
                <button type="button" onClick={() => setVehicles(vehicles.filter((_, i) => i !== idx))} className="text-red-400 hover:text-red-300">Remove</button>
              </div>
            ))}
            <div className="flex flex-wrap items-end gap-3">
              <Input label="Registration No" id="new-veh-reg" placeholder="KA-01-AB-1234" className="flex-1" />
              <Input label="Make / Model" id="new-veh-make" placeholder="Maruti Swift" className="flex-1" />
              <Button type="button" variant="secondary" onClick={() => {
                const regEl = document.getElementById("new-veh-reg") as HTMLInputElement;
                const makeEl = document.getElementById("new-veh-make") as HTMLInputElement;
                if (regEl && regEl.value.trim()) {
                  setVehicles([...vehicles, { regNo: regEl.value.trim(), make: makeEl.value.trim() }]);
                  regEl.value = "";
                  makeEl.value = "";
                }
              }}>+ Add Vehicle</Button>
            </div>
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
          <Button variant="secondary" onClick={() => navigate("/cases")}>
            Cancel
          </Button>
          <Button type="submit" isLoading={isSubmitting}>
            {isSubmitting ? "Creating..." : "Create Case"}
          </Button>
        </div>
      </form>
    </div>
  );
}
