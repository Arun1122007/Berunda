import { useEffect, useRef } from "react";
import cytoscape, { Core } from "cytoscape";
import Card from "@/components/ui/Card";

export default function LinkGraphPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);

  useEffect(() => {
    if (!containerRef.current || cyRef.current) return;

    const cy = cytoscape({
      container: containerRef.current,
      elements: [
        { data: { id: "placeholder", label: "Load data to view graph" } },
      ],
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
          },
        },
      ],
      layout: { name: "grid" },
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Link Graph</h1>
        <p className="mt-1 text-sm text-surface-400">
          Entity relationship graph — discover hidden links between persons,
          vehicles, and cases
        </p>
      </div>

      <Card className="overflow-hidden p-0">
        <div ref={containerRef} className="h-[600px] w-full" />
      </Card>
    </div>
  );
}
