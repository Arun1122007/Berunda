import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AiReviewPanel } from '@/features/ai-review/components/AiReviewPanel';
import Button from '@/components/ui/Button';

export default function FirAiReviewPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  // Mock suggestions
  const suggestions = [
    {
      id: '1',
      field: 'Location',
      suggestedValue: 'MG Road, Bangalore',
      sourceExcerpt: 'The incident occurred near MG Road, Bangalore around 10 PM.',
      confidence: 0.95,
      status: 'Unreviewed' as const
    },
    {
      id: '2',
      field: 'Crime Category',
      suggestedValue: 'Theft',
      sourceExcerpt: 'My wallet was stolen from my pocket.',
      confidence: 0.88,
      status: 'Unreviewed' as const
    }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between border-b pb-5">
        <div>
          <h1 className="text-2xl font-bold leading-7 text-slate-900 sm:truncate sm:text-3xl sm:tracking-tight">
            Review AI Extractions
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Review and approve the entities extracted from the uploaded document for FIR #{id}.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 flex space-x-3">
          <Button variant="outline" onClick={() => navigate(`/firs/${id}`)}>
            Back to FIR
          </Button>
        </div>
      </div>

      <AiReviewPanel suggestions={suggestions} />
    </div>
  );
}
