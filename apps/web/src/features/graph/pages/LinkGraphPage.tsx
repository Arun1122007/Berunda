import { useEffect, useRef } from "react";
import cytoscape, { Core, ElementDefinition } from "cytoscape";
import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { GraphData } from "@/types/api";

export default function LinkGraphPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);
  const { data: graphData, isLoading } = useQuery<GraphData>(
    "/graph?max_depth=2"
  );

  useEffect(() => {
    if (!containerRef.current) return;

    const elements: ElementDefinition[] = graphData
      ? [
          ...graphData.nodes.map((n) => ({
            data: { id: n.id, label: n.label },
          })),
          ...graphData.edges.map((e) => ({
            data: {
              id: `${e.source}-${e.target}`,
              source: e.source,
              target: e.target,
              label: e.label,
            },
          })),
        ]
      : [{ data: { id: "placeholder", label: "No data — load a case to view graph" } }];

    if (cyRef.current) {
      cyRef.current.destroy();
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#6366f1",
            label: "data(label)",
            color: "#e2e8f0",
            "font-size": "12px",
          },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#475569",
            "target-arrow-color": "#475569",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            label: "data(label)",
            "font-size": "10px",
            color: "#94a3b8",
          },
        },
      ],
      layout: { name: graphData && graphData.nodes.length > 0 ? "cose" : "grid" },
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, [graphData]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Link Graph</h1>
        <p className="mt-1 text-sm text-surface-400">
          Entity relationship graph — discover hidden links between persons,
          vehicles, and cases
        </p>
      </div>

      {isLoading && <LoadingSpinner />}

      <Card className="overflow-hidden p-0">
        <div ref={containerRef} className="h-[600px] w-full" />
      </Card>
    </div>
  );
}
