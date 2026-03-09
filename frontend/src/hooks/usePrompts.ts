import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchPrompts,
  createPrompt,
  updatePrompt,
  deletePrompt,
  PromptQueryParams,
  CreatePromptPayload,
  UpdatePromptPayload
} from "../api/prompts";

export function usePrompts(params?: PromptQueryParams) {
  return useQuery({
    queryKey: ["prompts", params],
    queryFn: () => fetchPrompts(params)
  });
}

export function useCreatePrompt() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreatePromptPayload) => createPrompt(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["prompts"] });
    }
  });
}

export function useUpdatePrompt() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: UpdatePromptPayload }) =>
      updatePrompt(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["prompts"] });
    }
  });
}

export function useDeletePrompt() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => deletePrompt(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["prompts"] });
    }
  });
}