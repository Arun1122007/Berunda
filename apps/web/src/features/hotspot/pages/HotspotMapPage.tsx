import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import Card from "@/components/ui/Card";

export default function HotspotMapPage() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<maplibregl.Map | null>(null);

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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-100">Hotspot Map</h1>
        <p className="mt-1 text-sm text-surface-400">
          Geographic crime density visualisation with district drill-down
        </p>
      </div>

      <Card className="overflow-hidden p-0">
        <div ref={mapContainer} className="h-[600px] w-full" />
      </Card>
    </div>
  );
}
