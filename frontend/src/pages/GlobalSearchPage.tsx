import React, { useState } from "react";
import { usePrompts } from "../hooks/usePrompts";
import PromptItem from "../components/prompts/PromptItem";
import PromptSearchBar from "../components/prompts/PromptSearchBar";
import LoadingSpinner from "../components/common/LoadingSpinner";

export default function GlobalSearchPage(): JSX.Element {
  const [search, setSearch] = useState("");
  const [tags, setTags] = useState<string[]>([]);

  const { data, isLoading, isError, refetch } = usePrompts({
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

  // Existing code with applied edits
    const prompts = data?.prompts ?? [];
  const hasQuery = search.trim().length > 0 || tags.length > 0;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Global Search</h1>

      <PromptSearchBar
        search={search}
        onSearchChange={setSearch}
        tags={tags}
        onTagsChange={setTags}
      />

      {!hasQuery && (
        <div style={styles.center}>
          <p>Search prompts across all collections.</p>
          <p style={styles.subtle}>
            Enter keywords or tags to begin searching.
          </p>
        </div>
      )}

      {hasQuery && (
        <>
          <div style={styles.resultHeader}>
            Results {search ? `for "${search}"` : ""} ({prompts.length})
        </div>

          {prompts.length === 0 ? (
            <div style={styles.center}>
              <p>No prompts found.</p>
              <p style={styles.subtle}>
                Try adjusting your search keywords or tags.
              </p>
    </div>
          ) : (
            <div style={styles.grid}>
              {prompts.map((prompt) => (
                <div key={prompt.id}>
                  <div style={styles.collectionLabel}>
                    Collection: {prompt.collection_id}
        </div>

                  <PromptItem prompt={prompt} onEdit={() => {}} />
    </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    flexDirection: "column",
    gap: "16px"
  },
  title: {
    margin: 0
  },
    grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
    gap: "16px"
  },
  resultHeader: {
    fontWeight: 600,
    color: "#374151"
  },
  center: {
    textAlign: "center",
    marginTop: "40px"
  },
  subtle: {
    color: "#6B7280",
    fontSize: "14px"
  },
  collectionLabel: {
    fontSize: "12px",
    color: "#6B7280",
    marginBottom: "4px"
  }
};