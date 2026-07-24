import { useState } from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Input from "@/components/ui/Input";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { PersonEntity, PersonEntityLink } from "@/types/api";
import { Search, User, Link as LinkIcon, ArrowRight } from "lucide-react";

export default function EntityPage() {
  const [searchName, setSearchName] = useState("");
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const { data: searchResults, isLoading: searching } = useQuery<{
    items: PersonEntity[];
    total: number;
  }>(searchName ? `/entities?name=${encodeURIComponent(searchName)}` : "/entities", {
    enabled: true,
  });

  const { data: entityDetail, isLoading: loadingDetail } = useQuery<PersonEntity>(
    selectedId ? `/entities/${selectedId}` : "",
    { enabled: selectedId !== null }
  );

  const { data: entityLinks, isLoading: loadingLinks } = useQuery<PersonEntityLink[]>(
    selectedId ? `/entities/${selectedId}/links` : "",
    { enabled: selectedId !== null }
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Entities</h1>
        <p className="mt-1 text-sm text-surface-400">
          Person entity resolution and link analysis
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-1 space-y-4">
          <Input
            placeholder="Search by name..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            icon={<Search size={16} />}
          />

          <Card>
            {searching ? (
              <LoadingSpinner />
            ) : !searchResults?.items?.length ? (
              <p className="py-8 text-center text-sm text-surface-500">No entities found</p>
            ) : (
              <div className="divide-y divide-surface-700 max-h-96 overflow-y-auto">
                {searchResults.items.map((entity) => (
                  <button
                    key={entity.personEntityId}
                    onClick={() => setSelectedId(entity.personEntityId)}
                    className={`w-full flex items-center gap-3 px-3 py-3 text-left transition-colors hover:bg-surface-700 ${
                      selectedId === entity.personEntityId ? "bg-berunda-600/20" : ""
                    }`}
                  >
                    <User size={18} className="text-berunda-400 shrink-0" />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-surface-200 truncate">
                        {entity.canonicalName}
                      </p>
                      <p className="text-xs text-surface-400">
                        {entity.gender || "—"} · District #{entity.primaryDistrictId || "—"}
                      </p>
                    </div>
                    <ArrowRight size={14} className="text-surface-500 shrink-0" />
                  </button>
                ))}
              </div>
            )}
          </Card>
        </div>

        <div className="lg:col-span-2 space-y-6">
          {!selectedId ? (
            <Card>
              <div className="flex flex-col items-center justify-center py-16 text-surface-500">
                <User size={48} className="mb-4 opacity-30" />
                <p className="text-sm">Select an entity to view details</p>
              </div>
            </Card>
          ) : (
            <>
              <Card
                header={
                  <div className="flex items-center gap-2">
                    <User size={18} className="text-berunda-400" />
                    <h2 className="font-semibold text-surface-100">
                      {entityDetail?.canonicalName || "Loading..."}
                    </h2>
                  </div>
                }
              >
                {loadingDetail ? (
                  <LoadingSpinner />
                ) : (
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-surface-400">Gender:</span>
                      <span className="ml-2 text-surface-200">{entityDetail?.gender || "—"}</span>
                    </div>
                    <div>
                      <span className="text-surface-400">District ID:</span>
                      <span className="ml-2 text-surface-200">{entityDetail?.primaryDistrictId || "—"}</span>
                    </div>
                    <div>
                      <span className="text-surface-400">Created:</span>
                      <span className="ml-2 text-surface-200">
                        {entityDetail?.createdAt ? new Date(entityDetail.createdAt).toLocaleDateString() : "—"}
                      </span>
                    </div>
                    <div>
                      <span className="text-surface-400">Updated:</span>
                      <span className="ml-2 text-surface-200">
                        {entityDetail?.updatedAt ? new Date(entityDetail.updatedAt).toLocaleDateString() : "—"}
                      </span>
                    </div>
                  </div>
                )}
              </Card>

              <Card
                header={
                  <div className="flex items-center gap-2">
                    <LinkIcon size={18} className="text-berunda-400" />
                    <h2 className="font-semibold text-surface-100">Linked Cases</h2>
                    {entityLinks && (
                      <Badge variant="info">{entityLinks.length} links</Badge>
                    )}
                  </div>
                }
              >
                {loadingLinks ? (
                  <LoadingSpinner />
                ) : !entityLinks?.length ? (
                  <p className="py-8 text-center text-sm text-surface-500">No linked cases</p>
                ) : (
                  <div className="divide-y divide-surface-700">
                    {entityLinks.map((link) => (
                      <div key={link.personEntityLinkId} className="flex items-center justify-between py-3">
                        <div>
                          <p className="text-sm font-medium text-surface-200">
                            Case #{link.caseMasterId}
                          </p>
                          <p className="text-xs text-surface-400">
                            Source: {link.sourceTable || "—"} · Record #{link.sourceRecordId || "—"}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          {link.confidence != null && (
                            <Badge variant={link.confidence > 0.8 ? "success" : "warning"}>
                              {(link.confidence * 100).toFixed(0)}%
                            </Badge>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
