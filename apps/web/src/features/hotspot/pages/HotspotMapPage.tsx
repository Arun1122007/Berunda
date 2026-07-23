import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useQuery } from "@/hooks/useApi";
import type { HotspotLayer } from "@/types/api";

export default function HotspotMapPage() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<maplibregl.Map | null>(null);
  const { data: layers, isLoading } = useQuery<HotspotLayer[]>(
    "/hotspots"
  );

  useEffect(() => {
    if (!mapContainer.current || mapInstance.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: [78.9629, 20.5937],
      zoom: 5,
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");
    mapInstance.current = map;

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, []);

  useEffect(() => {
    if (!mapInstance.current || !layers) return;
    const map = mapInstance.current;

    layers.forEach((layer) => {
      if (!layer.densityScore) return;
      const color = layer.densityScore > 0.7 ? "#ef4444" :
                    layer.densityScore > 0.4 ? "#f59e0b" : "#22c55e";
      new maplibregl.Marker({ color })
        .setLngLat([78.9629 + (layer.tileX ?? 0) * 0.5, 20.5937 + (layer.tileY ?? 0) * 0.5])
        .setPopup(new maplibregl.Popup().setText(`Density: ${(layer.densityScore * 100).toFixed(0)}%`))
        .addTo(map);
    });
  }, [layers]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Hotspot Map</h1>
        <p className="mt-1 text-sm text-surface-400">
          Geographic crime density visualisation with district drill-down
        </p>
      </div>

      {isLoading && <LoadingSpinner />}

      <Card className="overflow-hidden p-0">
        <div ref={mapContainer} className="h-[600px] w-full" />
      </Card>
    </div>
  );
}
