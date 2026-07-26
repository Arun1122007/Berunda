import { useState, ReactNode } from 'react';
import clsx from 'clsx';
import { ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-react';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';
import styles from './Table.module.css';

export interface Column<T> {
  key: string;
  header: string;
  sortable?: boolean;
  render?: (row: T) => ReactNode;
  className?: string;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  pagination?: ReactNode;
  onRowClick?: (row: T) => void;
  className?: string;
  rowKey: (row: T) => string | number;
}

function Table<T>({
  columns,
  data,
  loading = false,
  emptyMessage = 'No data available.',
  pagination,
  onRowClick,
  className,
  rowKey,
}: TableProps<T>) {
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc');

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortKey) return 0;
    const aVal = (a as Record<string, unknown>)[sortKey];
    const bVal = (b as Record<string, unknown>)[sortKey];
    if (aVal == null) return 1;
    if (bVal == null) return -1;
    const cmp =
      typeof aVal === 'number' && typeof bVal === 'number'
        ? aVal - bVal
        : String(aVal).localeCompare(String(bVal));
    return sortDir === 'asc' ? cmp : -cmp;
  });

  const renderSortIcon = (key: string) => {
    if (sortKey !== key) return <ChevronsUpDown size={14} />;
    return sortDir === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />;
  };

  return (
    <div className={clsx(styles.wrapper, className)} data-testid="table">
      <div className={clsx(loading && styles.loadingOverlay)}>
        <table className={styles.table}>
          <thead className={styles.thead}>
            <tr>
              {columns.map((col) => (
                <th
                  key={col.key}
                  className={clsx(
                    styles.th,
                    col.sortable && styles.sortable,
                    col.className,
                  )}
                  onClick={() => col.sortable && handleSort(col.key)}
                  aria-sort={
                    sortKey === col.key
                      ? sortDir === 'asc'
                        ? 'ascending'
                        : 'descending'
                      : undefined
                  }
                  data-testid={`table-th-${col.key}`}
                >
                  {col.header}
                  {col.sortable && (
                    <span className={styles.sortIcon}>
                      {renderSortIcon(col.key)}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className={styles.tbody}>
            {sortedData.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className={styles.emptyState}>
                  {loading ? 'Loading...' : emptyMessage}
                </td>
              </tr>
            ) : (
              sortedData.map((row) => (
                <tr
                  key={rowKey(row)}
                  className={clsx(styles.tr, onRowClick && styles.clickable)}
                  onClick={() => onRowClick?.(row)}
                  data-testid="table-row"
                >
                  {columns.map((col) => (
                    <td key={col.key} className={clsx(styles.td, col.className)}>
                      {col.render ? col.render(row) : (row as Record<string, unknown>)[col.key] as ReactNode}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
        {loading && <LoadingSpinner size="lg" />}
      </div>
      {pagination && <div className={styles.pagination}>{pagination}</div>}
    </div>
  );
}

export default Table;
