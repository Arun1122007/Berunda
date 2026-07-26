import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import Card, { CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/Card";

export default function FirEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  // Mock data
  const fir = {
    id,
    firNumber: 'FIR/2026/001',
    station: 'station-1',
    incidentDate: '2026-07-26',
    complaintText: 'This is the original text of the complaint...',
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    // simulate save
    setTimeout(() => {
      setLoading(false);
      navigate(`/firs/${id}`);
    }, 500);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold leading-7 text-slate-900 sm:truncate sm:text-3xl sm:tracking-tight">
          Edit FIR: {fir.firNumber}
        </h1>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          <CardHeader>
            <CardTitle>Update Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
              <Input label="FIR Number" name="firNumber" defaultValue={fir.firNumber} disabled />
              <Select label="Police Station" name="station" defaultValue={fir.station} required>
                <option value="station-1">Central Police Station</option>
                <option value="station-2">North Police Station</option>
              </Select>
              <Input label="Incident Date" name="incidentDate" type="date" defaultValue={fir.incidentDate} />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Complaint Text</label>
              <textarea
                name="complaintText"
                rows={4}
                defaultValue={fir.complaintText}
                className="block w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              />
            </div>
          </CardContent>
          <CardFooter className="flex justify-end space-x-3">
            <Button variant="outline" type="button" onClick={() => navigate(`/firs/${id}`)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={loading}>
              Save Changes
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
