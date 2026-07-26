import React, { useState } from 'react';
import Button from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { CheckCircle, XCircle, Edit2, AlertCircle } from 'lucide-react';

interface Suggestion {
  id: string;
  field: string;
  suggestedValue: string;
  sourceExcerpt: string;
  confidence: number;
  status: 'Unreviewed' | 'Accepted' | 'Rejected' | 'Edited';
  finalValue?: string;
}

export function AiReviewPanel({ suggestions: initialSuggestions }: { suggestions: Suggestion[] }) {
  const [suggestions, setSuggestions] = useState(initialSuggestions);

  const handleAction = (id: string, action: 'Accept' | 'Reject' | 'Edit', newValue?: string) => {
    setSuggestions(prev => prev.map(s => {
      if (s.id === id) {
        if (action === 'Accept') return { ...s, status: 'Accepted', finalValue: s.suggestedValue };
        if (action === 'Reject') return { ...s, status: 'Rejected', finalValue: undefined };
        if (action === 'Edit') return { ...s, status: 'Edited', finalValue: newValue };
      }
      return s;
    }));
  };

  return (
    <div className="space-y-4">
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <AlertCircle className="h-5 w-5 text-yellow-400" aria-hidden="true" />
          </div>
          <div className="ml-3">
            <p className="text-sm text-yellow-700">
              <strong>Requires Officer Review:</strong> The following entities were extracted automatically. They are suggestions and must not be considered official until reviewed and approved.
            </p>
          </div>
        </div>
      </div>

      {suggestions.map((suggestion) => (
        <Card key={suggestion.id} className={suggestion.status === 'Unreviewed' ? 'border-blue-200 shadow-sm' : 'opacity-80'}>
          <CardHeader className="py-3 bg-slate-50 flex flex-row items-center justify-between">
            <CardTitle className="text-sm font-medium text-slate-700">
              {suggestion.field}: {suggestion.suggestedValue}
            </CardTitle>
            <div className="text-xs text-slate-500">Confidence: {(suggestion.confidence * 100).toFixed(0)}%</div>
          </CardHeader>
          <CardContent className="pt-4 pb-4">
            <p className="text-xs text-slate-500 mb-3 italic">
              Source: "{suggestion.sourceExcerpt}"
            </p>
            
            <div className="flex items-center space-x-2">
              {suggestion.status === 'Unreviewed' ? (
                <>
                  <Button size="sm" variant="outline" className="text-green-600 border-green-200 hover:bg-green-50" onClick={() => handleAction(suggestion.id, 'Accept')}>
                    <CheckCircle className="h-4 w-4 mr-1" /> Accept
                  </Button>
                  <Button size="sm" variant="outline" className="text-red-600 border-red-200 hover:bg-red-50" onClick={() => handleAction(suggestion.id, 'Reject')}>
                    <XCircle className="h-4 w-4 mr-1" /> Reject
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => {
                    const val = prompt('Edit value:', suggestion.suggestedValue);
                    if (val) handleAction(suggestion.id, 'Edit', val);
                  }}>
                    <Edit2 className="h-4 w-4 mr-1" /> Edit
                  </Button>
                </>
              ) : (
                <div className="text-sm font-medium">
                  {suggestion.status === 'Accepted' && <span className="text-green-600 flex items-center"><CheckCircle className="h-4 w-4 mr-1"/> Accepted</span>}
                  {suggestion.status === 'Rejected' && <span className="text-red-600 flex items-center"><XCircle className="h-4 w-4 mr-1"/> Rejected</span>}
                  {suggestion.status === 'Edited' && <span className="text-blue-600 flex items-center"><Edit2 className="h-4 w-4 mr-1"/> Edited: {suggestion.finalValue}</span>}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}

      {suggestions.every(s => s.status !== 'Unreviewed') && suggestions.length > 0 && (
        <div className="mt-4 flex justify-end">
          <Button onClick={() => alert('Review saved')}>Save Final Review</Button>
        </div>
      )}
    </div>
  );
}
