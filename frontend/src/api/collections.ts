import { apiRequest } from "./client";

export interface Collection {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface CollectionsResponse {
  collections: Collection[];
  total: number;
}

export interface CreateCollectionPayload {
  name: string;
  description?: string;
}

export async function fetchCollections(): Promise<CollectionsResponse> {
  return apiRequest<CollectionsResponse>("/collections");
}

export async function fetchCollection(collectionId: string): Promise<Collection> {
  return apiRequest<Collection>(`/collections/${collectionId}`);
}

export async function createCollection(
  payload: CreateCollectionPayload
): Promise<Collection> {
  return apiRequest<Collection>("/collections", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function deleteCollection(collectionId: string): Promise<void> {
  await apiRequest<void>(`/collections/${collectionId}`, {
    method: "DELETE"
  });
}