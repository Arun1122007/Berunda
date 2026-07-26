import React from 'react';
import clsx from 'clsx';

export function Table({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={clsx("overflow-x-auto shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg", className)}>
      <table className="min-w-full divide-y divide-slate-300">{children}</table>
    </div>
  );
}

export function TableHead({ children }: { children: React.ReactNode }) {
  return <thead className="bg-slate-50">{children}</thead>;
}

export function TableBody({ children }: { children: React.ReactNode }) {
  return <tbody className="divide-y divide-slate-200 bg-white">{children}</tbody>;
}

export function TableRow({ children, className, onClick }: { children: React.ReactNode; className?: string; onClick?: () => void }) {
  return <tr className={clsx(className, onClick && "cursor-pointer hover:bg-slate-50")} onClick={onClick}>{children}</tr>;
}

export function TableHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <th
      scope="col"
      className={clsx("px-3 py-3.5 text-left text-sm font-semibold text-slate-900", className)}
    >
      {children}
    </th>
  );
}

export function TableCell({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <td className={clsx("whitespace-nowrap px-3 py-4 text-sm text-slate-500", className)}>
      {children}
    </td>
  );
}
