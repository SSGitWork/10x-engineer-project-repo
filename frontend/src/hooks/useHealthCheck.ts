import { useQuery } from "@tanstack/react-query";
import { apiRequest } from "../api/client";

interface HealthResponse {
  status: string;
  version: string;
}

async function fetchHealth(): Promise<HealthResponse> {
  return apiRequest<HealthResponse>("/health");
}

export function useHealthCheck() {
  return useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    refetchInterval: 30000
  });
}