import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Card, { CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/Card";
import Button from '@/components/ui/Button';
import { Upload, File, AlertCircle } from 'lucide-react';
import { apiClient } from '@/services/api-client';

export default function FirUploadPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selected = e.target.files[0];
      if (selected.size > 200 * 1024 * 1024) { // 200MB limit
        setError('File size exceeds 200MB limit.');
        setFile(null);
        return;
      }
      setError(null);
      setFile(selected);
    }
  };

  const handleUpload = async () => {
    if (!file || !id) return;
    
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await apiClient.upload(`/fir/${id}/evidence`, formData);
      navigate(`/firs/${id}`);
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold leading-7 text-slate-900 sm:truncate sm:text-3xl sm:tracking-tight">
          Upload FIR Document
        </h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Source Document</CardTitle>
          <p className="text-sm text-slate-500">
            Upload a scanned PDF or text document of the original FIR. Maximum size 200MB.
          </p>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-200 flex items-center">
              <AlertCircle className="h-4 w-4 mr-2" />
              {error}
            </div>
          )}
          
          {!file ? (
            <div className="mt-2 flex justify-center rounded-lg border border-dashed border-slate-900/25 px-6 py-10">
              <div className="text-center">
                <Upload className="mx-auto h-12 w-12 text-slate-300" aria-hidden="true" />
                <div className="mt-4 flex text-sm leading-6 text-slate-600 justify-center">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer rounded-md bg-white font-semibold text-blue-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-blue-600 focus-within:ring-offset-2 hover:text-blue-500"
                  >
                    <span>Upload a file</span>
                    <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileChange} accept=".pdf,.txt,.docx" />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs leading-5 text-slate-600">PDF, TXT, DOCX up to 200MB</p>
              </div>
            </div>
          ) : (
            <div className="flex items-center p-4 border rounded-md border-slate-200">
              <File className="h-8 w-8 text-blue-500 mr-3" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-900 truncate">{file.name}</p>
                <p className="text-sm text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <Button variant="outline" size="sm" onClick={() => setFile(null)}>
                Remove
              </Button>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-end space-x-3">
          <Button variant="outline" onClick={() => navigate(`/firs/${id}`)}>
            Cancel
          </Button>
          <Button onClick={handleUpload} disabled={!file} isLoading={loading}>
            Upload
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
