import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, SlidersHorizontal, X, ChevronDown, ChevronUp, ArrowLeft, ArrowRight, FileText } from "lucide-react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { apiClient } from "@/services/api-client";
import { formatDate } from "@/lib";
import type { SearchFilters, SearchResultItem, SearchResponse } from "@/types/api";

const PAGE_SIZE = 20;

const STATUS_OPTIONS = [
  { value: "", label: "All Statuses" },
  { value: "1", label: "Registered" },
  { value: "2", label: "Under Investigation" },
  { value: "3", label: "Charge Sheet Filed" },
  { value: "4", label: "Trial" },
  { value: "5", label: "Convicted" },
  { value: "6", label: "Acquitted" },
  { value: "7", label: "Closed" },
];

const POLICE_STATIONS = [
  { value: "", label: "All Stations" },
  { value: "1", label: "Bengaluru City" },
  { value: "2", label: "Mysuru" },
  { value: "3", label: "Hubballi-Dharwad" },
  { value: "4", label: "Mangaluru City" },
  { value: "5", label: "Belagavi" },
  { value: "6", label: "Kalaburagi" },
];

const CRIME_MAJOR_HEADS = [
  { value: "", label: "All Heads" },
  { value: "1", label: "Cybercrime / Financial Fraud" },
  { value: "2", label: "Theft & Burglary" },
  { value: "3", label: "Narcotics & NDPS" },
  { value: "4", label: "Violent Assault & IPC 307" },
  { value: "5", label: "Organized Syndicate Activity" },
  { value: "6", label: "Property Dispute" },
  { value: "7", label: "Missing Person" },
  { value: "8", label: "Sexual Offense" },
];

export default function SearchPage() {
  const navigate = useNavigate();

  const [query, setQuery] = useState("");
  const [crimeNo, setCrimeNo] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [statusId, setStatusId] = useState("");
  const [policeStationId, setPoliceStationId] = useState("");
  const [crimeMajorHeadId, setCrimeMajorHeadId] = useState("");
  const [personName, setPersonName] = useState("");
  const [vehicleNumber, setVehicleNumber] = useState("");
  const [semantic, setSemantic] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  const buildFilters = (pageNum: number): SearchFilters => ({
    query: query || undefined,
    crimeNo: crimeNo || undefined,
    dateFrom: dateFrom || undefined,
    dateTo: dateTo || undefined,
    statusId: statusId ? Number(statusId) : undefined,
    policeStationId: policeStationId ? Number(policeStationId) : undefined,
    crimeMajorHeadId: crimeMajorHeadId ? Number(crimeMajorHeadId) : undefined,
    personName: personName || undefined,
    vehicleNumber: vehicleNumber || undefined,
    page: pageNum,
    pageSize: PAGE_SIZE,
    semantic,
  });

  const handleSearch = async (pageNum = 1) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);
    try {
      const filters = buildFilters(pageNum);
      const response = await apiClient.post<SearchResponse>("/search", filters);
      setResults(response.items);
      setTotal(response.total);
      setPage(response.page);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed");
      setResults([]);
      setTotal(0);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSearch(1);
  };

  const goToPage = (p: number) => {
    if (p < 1 || p > totalPages) return;
    handleSearch(p);
  };

  const clearFilters = () => {
    setQuery("");
    setCrimeNo("");
    setDateFrom("");
    setDateTo("");
    setStatusId("");
    setPoliceStationId("");
    setCrimeMajorHeadId("");
    setPersonName("");
    setVehicleNumber("");
    setSemantic(false);
    setResults([]);
    setTotal(0);
    setPage(1);
    setHasSearched(false);
    setError(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-berunda-600/10 text-berunda-400">
            <Search size={22} />
          </span>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-surface-100">
              Search
            </h1>
            <p className="text-sm text-surface-400">
              Search across FIR cases, persons, vehicles, and evidence
            </p>
          </div>
        </div>
        {hasSearched && (
          <Button variant="ghost" size="sm" onClick={clearFilters}>
            <X size={14} className="mr-1.5" /> Clear
          </Button>
        )}
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          <div className="flex items-center gap-3">
            <div className="relative flex-1">
              <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-surface-400" size={18} />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search by case details, person name, vehicle, or any keyword..."
                className="w-full rounded-lg border border-surface-600 bg-surface-900 py-2.5 pl-10 pr-4 text-sm text-surface-100 placeholder-surface-500 transition-colors focus:outline-none focus:ring-2 focus:ring-berunda-500"
              />
            </div>
            <Button type="submit" isLoading={isLoading}>
              <Search size={16} className="mr-1.5" /> Search
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => setShowAdvanced(!showAdvanced)}
            >
              <SlidersHorizontal size={15} className="mr-1.5" />
              Filters
              {showAdvanced ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </Button>
          </div>

          <div className="mt-3 flex items-center gap-3">
            <label className="flex items-center gap-2 cursor-pointer">
              <div className="relative">
                <input
                  type="checkbox"
                  checked={semantic}
                  onChange={(e) => setSemantic(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="h-5 w-9 rounded-full bg-surface-600 after:absolute after:left-[2px] after:top-[2px] after:h-4 after:w-4 after:rounded-full after:bg-surface-300 after:transition-all peer-checked:bg-berunda-600 peer-checked:after:translate-x-full" />
              </div>
              <span className="text-sm text-surface-300">Semantic Search</span>
            </label>
            {semantic && (
              <span className="text-xs text-berunda-400">
                Uses AI embeddings to find semantically similar cases
              </span>
            )}
          </div>

          {showAdvanced && (
            <div className="mt-4 grid gap-4 border-t border-surface-700 pt-4 sm:grid-cols-2 lg:grid-cols-3">
              <Input
                label="Crime Number"
                placeholder="e.g. CR-2026-0001"
                value={crimeNo}
                onChange={(e) => setCrimeNo(e.target.value)}
              />
              <Input
                label="Person Name"
                placeholder="Search by name"
                value={personName}
                onChange={(e) => setPersonName(e.target.value)}
              />
              <Input
                label="Vehicle Number"
                placeholder="e.g. KA-01-AB-1234"
                value={vehicleNumber}
                onChange={(e) => setVehicleNumber(e.target.value)}
              />
              <div>
                <label className="mb-1.5 block text-sm font-medium text-surface-300">Date From</label>
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 transition-colors focus:outline-none focus:ring-2 focus:ring-berunda-500"
                />
              </div>
              <div>
                <label className="mb-1.5 block text-sm font-medium text-surface-300">Date To</label>
                <input
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 transition-colors focus:outline-none focus:ring-2 focus:ring-berunda-500"
                />
              </div>
              <div>
                <label className="mb-1.5 block text-sm font-medium text-surface-300">Status</label>
                <select
                  value={statusId}
                  onChange={(e) => setStatusId(e.target.value)}
                  className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 focus:outline-none focus:ring-2 focus:ring-berunda-500"
                >
                  {STATUS_OPTIONS.map((o) => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="mb-1.5 block text-sm font-medium text-surface-300">Police Station</label>
                <select
                  value={policeStationId}
                  onChange={(e) => setPoliceStationId(e.target.value)}
                  className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 focus:outline-none focus:ring-2 focus:ring-berunda-500"
                >
                  {POLICE_STATIONS.map((o) => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="mb-1.5 block text-sm font-medium text-surface-300">Crime Major Head</label>
                <select
                  value={crimeMajorHeadId}
                  onChange={(e) => setCrimeMajorHeadId(e.target.value)}
                  className="w-full rounded-lg border border-surface-600 bg-surface-900 px-3 py-2 text-sm text-surface-100 focus:outline-none focus:ring-2 focus:ring-berunda-500"
                >
                  {CRIME_MAJOR_HEADS.map((o) => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </form>
      </Card>

      {error && (
        <div className="rounded-lg border border-red-700 bg-red-900/20 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {isLoading && (
        <div className="flex items-center justify-center py-16">
          <LoadingSpinner size="lg" />
        </div>
      )}

      {!isLoading && hasSearched && results.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <FileText size={48} className="text-surface-600 mb-4" />
          <h3 className="text-lg font-semibold text-surface-300">No results found</h3>
          <p className="mt-1 text-sm text-surface-500 max-w-md">
            Try adjusting your search query or filters. If you&apos;re looking for specific case details, try using the crime number or person name.
          </p>
          <Button variant="secondary" size="sm" className="mt-4" onClick={clearFilters}>
            Clear Filters
          </Button>
        </div>
      )}

      {!isLoading && hasSearched && results.length > 0 && (
        <>
          <div className="flex items-center justify-between">
            <p className="text-sm text-surface-400">
              Found <span className="font-medium text-surface-200">{total}</span> result{total !== 1 ? "s" : ""}
              {semantic && (
                <Badge variant="info" className="ml-2">Semantic</Badge>
              )}
            </p>
          </div>

          <div className="space-y-3">
            {results.map((item) => (
              <div
                key={item.caseMasterId}
                className="cursor-pointer rounded-xl border border-surface-700 bg-surface-800 p-5 transition-all duration-200 hover:border-berunda-700/50 hover:shadow-lg hover:shadow-berunda-900/10"
                onClick={() => navigate(`/cases/${item.caseMasterId}`)}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="text-base font-semibold text-surface-100 truncate">
                        {item.crimeNo || `Case #${item.caseMasterId}`}
                      </h3>
                      <Badge variant="info">ID: {item.caseMasterId}</Badge>
                    </div>
                    <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-surface-400">
                      <span>{formatDate(item.crimeRegisteredDate)}</span>
                      {item.policeStationId && <span>Station #{item.policeStationId}</span>}
                      {item.caseStatusId && <span>Status: {item.caseStatusId}</span>}
                    </div>
                    {item.briefFacts && (
                      <p className="mt-2 line-clamp-2 text-sm text-surface-500">
                        {item.briefFacts}
                      </p>
                    )}
                  </div>
                  <div className="shrink-0 text-right">
                    {item.confidence != null && (
                      <div className="mb-1">
                        <span className="text-xs text-surface-500">Confidence </span>
                        <span className="text-sm font-semibold text-berunda-400">
                          {(item.confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                    )}
                    {item.matchReason && (
                      <p className="max-w-[200px] text-xs text-surface-500 truncate" title={item.matchReason}>
                        {item.matchReason}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 pt-2">
              <Button
                variant="secondary"
                size="sm"
                disabled={page <= 1}
                onClick={() => goToPage(page - 1)}
              >
                <ArrowLeft size={14} className="mr-1" /> Previous
              </Button>
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter((p) => p === 1 || p === totalPages || Math.abs(p - page) <= 2)
                .map((p, idx, arr) => (
                  <span key={p} className="flex items-center">
                    {idx > 0 && arr[idx - 1] !== p - 1 && (
                      <span className="px-1 text-surface-500">...</span>
                    )}
                    <button
                      onClick={() => goToPage(p)}
                      className={`flex h-8 w-8 items-center justify-center rounded-lg text-sm font-medium transition-colors ${
                        p === page
                          ? "bg-berunda-600 text-white"
                          : "text-surface-400 hover:bg-surface-700 hover:text-surface-200"
                      }`}
                    >
                      {p}
                    </button>
                  </span>
                ))}
              <Button
                variant="secondary"
                size="sm"
                disabled={page >= totalPages}
                onClick={() => goToPage(page + 1)}
              >
                Next <ArrowRight size={14} className="ml-1" />
              </Button>
            </div>
          )}
        </>
      )}

      {!hasSearched && !isLoading && (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <Search size={48} className="text-surface-600 mb-4" />
          <h3 className="text-lg font-semibold text-surface-300">Search across all case data</h3>
          <p className="mt-1 text-sm text-surface-500 max-w-md">
            Enter a keyword above to search across FIR cases, persons, vehicles, and evidence records. Use the advanced filters to narrow down by date, status, station, or crime type.
          </p>
        </div>
      )}
    </div>
  );
}
