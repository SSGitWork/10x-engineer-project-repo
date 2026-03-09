import { apiRequest } from "./client";

export interface Prompt {
  id: string;
  title: string;
  content: string;
  description?: string;
  collection_id: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface PromptsResponse {
  prompts: Prompt[];
  total: number;
}

export interface CreatePromptPayload {
  title: string;
  content: string;
  description?: string;
  collection_id: string;
  tags?: string[];
}

export interface UpdatePromptPayload {
  title?: string;
  content?: string;
  description?: string;
  collection_id?: string;
  tags?: string[];
}

export interface PromptQueryParams {
  collection_id?: string;
  search?: string;
  tags?: string[];
}

function buildQuery(params?: PromptQueryParams): string {
  if (!params) return "";

  const query = new URLSearchParams();

  if (params.collection_id) {
    query.append("collection_id", params.collection_id);
  }

  if (params.search) {
    query.append("search", params.search);
  }

  if (params.tags && params.tags.length > 0) {
    query.append("tags", params.tags.join(","));
  }

  const queryString = query.toString();
  return queryString ? `?${queryString}` : "";
}

export async function fetchPrompts(
  params?: PromptQueryParams
): Promise<PromptsResponse> {
  const query = buildQuery(params);
  return apiRequest<PromptsResponse>(`/prompts${query}`);
}

export async function fetchPrompt(promptId: string): Promise<Prompt> {
  return apiRequest<Prompt>(`/prompts/${promptId}`);
}

export async function createPrompt(payload: CreatePromptPayload): Promise<Prompt> {
  return apiRequest<Prompt>("/prompts", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function updatePrompt(
  promptId: string,
  payload: UpdatePromptPayload
): Promise<Prompt> {
  return apiRequest<Prompt>(`/prompts/${promptId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export async function deletePrompt(promptId: string): Promise<void> {
  await apiRequest<void>(`/prompts/${promptId}`, {
    method: "DELETE"
  });
}
