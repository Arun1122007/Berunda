import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/Table';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import { useQuery } from '@/hooks/useApi';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

export default function FirListPage() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const pageSize = 20;

  const { data, isLoading, error } = useQuery<any>(
    `/fir?page=${page}&page_size=${pageSize}`
  );

  const firs = data?.items ?? [];

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
          {isLoading && (
            <TableRow>
              <TableCell colSpan={5} className="text-center py-10">
                <LoadingSpinner />
              </TableCell>
            </TableRow>
          )}
          {error && (
            <TableRow>
              <TableCell colSpan={5} className="text-center py-10 text-red-500">
                Error loading FIRs: {error}
              </TableCell>
            </TableRow>
          )}
          {!isLoading && !error && firs.length === 0 && (
            <TableRow>
              <TableCell colSpan={5} className="text-center py-10 text-slate-500">
                No FIRs found.
              </TableCell>
            </TableRow>
          )}
          {firs.map((fir: any) => (
            <TableRow key={fir.fir_id} onClick={() => navigate(`/firs/${fir.fir_id}`)}>
              <TableCell className="font-medium text-slate-900">{fir.fir_number}</TableCell>
              <TableCell>{fir.incident_date}</TableCell>
              <TableCell>Station {fir.police_station_id}</TableCell>
              <TableCell>
                <Badge variant={fir.status === 'Draft' ? 'secondary' : 'default'}>{fir.status}</Badge>
              </TableCell>
              <TableCell className="text-right font-medium">
                <a href={`/firs/${fir.fir_id}`} className="text-blue-600 hover:text-blue-900" onClick={(e) => { e.preventDefault(); navigate(`/firs/${fir.fir_id}`); }}>
                  View<span className="sr-only">, {fir.fir_number}</span>
                </a>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
