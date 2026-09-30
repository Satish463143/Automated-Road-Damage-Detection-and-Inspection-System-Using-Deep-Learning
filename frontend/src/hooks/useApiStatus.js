import { useCallback, useEffect, useState } from "react";

import { api } from "../services/api";

export function useApiStatus() {
  const [status, setStatus] = useState({
    loading: true,
    backend: "checking",
    database: "checking",
    model: "checking",
  });

  const refresh = useCallback(async () => {
    setStatus((current) => ({ ...current, loading: true }));

    try {
      const data = await api.health();

      setStatus({
        loading: false,
        backend: data.status || "unknown",
        database: data.database || "unknown",
        model: data.model || "unknown",
      });
    } catch {
      setStatus({
        loading: false,
        backend: "offline",
        database: "unknown",
        model: "unknown",
      });
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { ...status, refresh };
}
