import React, { useState } from "react";
import { usePrompts } from "../../hooks/usePrompts";
import { Prompt } from "../../api/prompts";
import PromptItem from "./PromptItem";
import PromptForm from "./PromptForm";
import PromptSearchBar from "./PromptSearchBar";
import LoadingSpinner from "../common/LoadingSpinner";
import { useCollections } from "../../hooks/useCollections";

interface PromptsListProps {
  collectionId?: string;
}

export default function PromptsList({ collectionId }: PromptsListProps): JSX.Element {
    const [search, setSearch] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [editingPrompt, setEditingPrompt] = useState<Prompt | null>(null);
  const [collectionFilter, setCollectionFilter] = useState<string>("all");

  const { data: collectionsData } = useCollections();
  const collections = collectionsData?.collections ?? [];

  const { data, isLoading, isError, refetch } = usePrompts({
    collection_id: collectionFilter === "all" ? collectionId : collectionFilter,
    search,
    tags
  });

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError) {
    return (
      <div style={styles.center}>
        <p>Failed to load prompts.</p>
        <button onClick={() => refetch()}>Retry</button>
      </div>
    );
  }

  const prompts = data?.prompts ?? [];

    return (
    <div>
      <div style={styles.toolbar}>
        <PromptForm
          collectionId={collectionId ?? ""}
          editingPrompt={editingPrompt}
          onClose={() => setEditingPrompt(null)}
        />

        <div style={styles.filters}>
          <label>
            Collection:
            <select
              value={collectionFilter}
              onChange={(e) => setCollectionFilter(e.target.value)}
              style={styles.select}
            >
              <option value="all">All Collections</option>

              {collections.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            View:
            <select style={styles.select}>
              <option>Grid</option>
            </select>
          </label>
        </div>
      </div>

            <PromptSearchBar
        search={search}
        onSearchChange={setSearch}
        tags={tags}
        onTagsChange={setTags}
      />

            {prompts.length === 0 ? (
        <div style={styles.emptyCard}>
          <h3>No prompts yet</h3>
          <p>Create your first prompt and optionally assign it to a collection.</p>
        </div>
      ) : (
        <div style={styles.grid}>
          {prompts.map((prompt) => (
            <PromptItem
              key={prompt.id}
              prompt={prompt}
              onEdit={setEditingPrompt}
            />
          ))}
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  toolbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "12px"
  },
  filters: {
    display: "flex",
    gap: "12px",
    alignItems: "center"
  },
  select: {
    marginLeft: "6px",
    padding: "6px",
    borderRadius: "6px",
    border: "1px solid #E5E7EB"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "16px",
    marginTop: "16px"
  },
    center: {
    textAlign: "center",
    marginTop: "40px"
  },
  emptyCard: {
    marginTop: "24px",
    border: "1px solid #E5E7EB",
    borderRadius: "8px",
    padding: "28px",
    textAlign: "center",
    background: "#FFFFFF"
  }
};

