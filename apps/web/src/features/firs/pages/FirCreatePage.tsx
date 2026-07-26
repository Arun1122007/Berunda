import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import Card, { CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/Card";
import { apiClient } from '@/services/api-client';

export default function FirCreatePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData.entries());

    try {
      // API call to backend
      const result = await apiClient.post<{ id: string }>('/firs', data);
      navigate(`/firs/${result.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to create FIR');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold leading-7 text-slate-900 sm:truncate sm:text-3xl sm:tracking-tight">
          Register New FIR
        </h1>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          <CardHeader>
            <CardTitle>FIR Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {error && <div className="p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-200">{error}</div>}
            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
              <Input label="FIR Number" name="firNumber" required placeholder="e.g. 123/2026" />
              <Input label="Registration Date" name="registrationDate" type="date" required />
              <Select label="Police Station" name="station" required>
                <option value="">Select a station...</option>
                <option value="station-1">Central Police Station</option>
                <option value="station-2">North Police Station</option>
              </Select>
              <Input label="Incident Date" name="incidentDate" type="date" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Complaint Text</label>
              <textarea
                name="complaintText"
                rows={4}
                className="block w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              />
            </div>
          </CardContent>
          <CardFooter className="flex justify-end space-x-3">
            <Button variant="outline" type="button" onClick={() => navigate('/firs')}>
              Cancel
            </Button>
            <Button type="submit" isLoading={loading}>
              Save as Draft
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
