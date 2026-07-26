import { useState, useEffect, useRef, useCallback } from "react";

export interface WebSocketEvent {
  event: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

interface UseWebSocketReturn {
  isConnected: boolean;
  events: WebSocketEvent[];
  lastEvent: WebSocketEvent | null;
  clearEvents: () => void;
}

export function useWebSocket(url: string = "/api/v1/notifications/ws"): UseWebSocketReturn {
  const [isConnected, setIsConnected] = useState(false);
  const [events, setEvents] = useState<WebSocketEvent[]>([]);
  const [lastEvent, setLastEvent] = useState<WebSocketEvent | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const connect = useCallback(() => {
    try {
      const token = sessionStorage.getItem("auth_token") || localStorage.getItem("berunda_access_token") || "";
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const host = window.location.host;
      const wsUrl = url.startsWith("ws") ? url : `${protocol}//${host}${url}?token=${encodeURIComponent(token)}`;

      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const newEvent: WebSocketEvent = {
            event: data.event || "UNKNOWN_EVENT",
            payload: data.payload || {},
            timestamp: new Date().toISOString(),
          };
          setLastEvent(newEvent);
          setEvents((prev) => [newEvent, ...prev].slice(0, 50));
        } catch {
          // ignore malformed websocket messages
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        // auto-reconnect after 5 seconds in production
        reconnectTimeoutRef.current = window.setTimeout(() => {
          connect();
        }, 5000);
      };

      ws.onerror = () => {
        setIsConnected(false);
      };
    } catch {
      setIsConnected(false);
    }
  }, [url]);

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  const clearEvents = useCallback(() => {
    setEvents([]);
    setLastEvent(null);
  }, []);

  return { isConnected, events, lastEvent, clearEvents };
}
