import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/Button';
import { Tabs } from '@/components/ui/Tabs';
import { Badge } from '@/components/ui/Badge';

export default function FirDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  // Mock data
  const fir = {
    id,
    firNumber: 'FIR/2026/001',
    status: 'Under Investigation',
    registrationDate: '2026-07-26',
    station: 'Central Police Station',
    complaintText: 'This is the original text of the complaint...',
    aiProcessingStatus: 'Completed',
  };

  const tabs = [
    {
      id: 'summary',
      label: 'Summary',
      content: (
        <div className="space-y-6">
          <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-base font-semibold leading-6 text-gray-900">Complaint Details</h3>
              <div className="mt-2 max-w-xl text-sm text-gray-500">
                <p>{fir.complaintText}</p>
              </div>
              <div className="mt-5">
                <Button type="button" onClick={() => navigate(`/firs/${id}/edit`)}>
                  Edit Details
                </Button>
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      id: 'entities',
      label: 'Entities',
      content: (
        <div className="bg-white shadow sm:rounded-lg p-6">
          <p className="text-sm text-gray-500">No entities identified yet. <a href="#" className="text-blue-600">Review AI extractions</a> to add entities.</p>
        </div>
      ),
    },
    {
      id: 'timeline',
      label: 'Timeline',
      content: (
        <div className="bg-white shadow sm:rounded-lg p-6">
          <p className="text-sm text-gray-500">Timeline feature coming soon.</p>
        </div>
      )
    }
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between border-b pb-5">
        <div>
          <h1 className="text-2xl font-bold leading-7 text-slate-900 sm:truncate sm:text-3xl sm:tracking-tight">
            {fir.firNumber}
          </h1>
          <div className="mt-2 flex items-center space-x-3 text-sm text-slate-500">
            <span>{fir.station}</span>
            <span>&middot;</span>
            <span>{fir.registrationDate}</span>
            <span>&middot;</span>
            <Badge>{fir.status}</Badge>
          </div>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 flex space-x-3">
          <Button variant="outline" onClick={() => navigate(`/firs/${id}/upload`)}>
            Upload Document
          </Button>
          <Button onClick={() => navigate(`/firs/${id}/ai-review`)}>
            AI Review {fir.aiProcessingStatus === 'Completed' && <span className="ml-2 relative flex h-2 w-2"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span><span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span></span>}
          </Button>
        </div>
      </div>

      <Tabs tabs={tabs} />
    </div>
  );
}
