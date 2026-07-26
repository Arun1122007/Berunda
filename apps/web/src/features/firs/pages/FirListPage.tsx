import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/Table';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';

// Mock FIR Type - will be replaced with domain types
interface FIR {
  id: string;
  firNumber: string;
  registrationDate: string;
  station: string;
  status: 'Draft' | 'Registered' | 'Under Investigation' | 'Closed';
}

const mockData: FIR[] = [
  { id: '1', firNumber: 'FIR/2026/001', registrationDate: '2026-07-26', station: 'Central Station', status: 'Draft' },
  { id: '2', firNumber: 'FIR/2026/002', registrationDate: '2026-07-25', station: 'North Station', status: 'Registered' },
];

export default function FirListPage() {
  const navigate = useNavigate();

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold leading-7 text-slate-900 sm:truncate sm:text-3xl sm:tracking-tight">
            First Information Reports
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            A list of all FIRs in the system including their number, date, station, and status.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <Button onClick={() => navigate('/firs/new')}>
            Register New FIR
          </Button>
        </div>
      </div>

      <Table>
        <TableHead>
          <TableRow>
            <TableHeader>FIR Number</TableHeader>
            <TableHeader>Date</TableHeader>
            <TableHeader>Station</TableHeader>
            <TableHeader>Status</TableHeader>
            <TableHeader className="relative px-3 py-3.5"><span className="sr-only">Actions</span></TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          {mockData.map((fir) => (
            <TableRow key={fir.id} onClick={() => navigate(`/firs/${fir.id}`)}>
              <TableCell className="font-medium text-slate-900">{fir.firNumber}</TableCell>
              <TableCell>{fir.registrationDate}</TableCell>
              <TableCell>{fir.station}</TableCell>
              <TableCell>
                <Badge variant={fir.status === 'Draft' ? 'secondary' : 'default'}>{fir.status}</Badge>
              </TableCell>
              <TableCell className="text-right font-medium">
                <a href={`/firs/${fir.id}`} className="text-blue-600 hover:text-blue-900" onClick={(e) => { e.preventDefault(); navigate(`/firs/${fir.id}`); }}>
                  View<span className="sr-only">, {fir.firNumber}</span>
                </a>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
