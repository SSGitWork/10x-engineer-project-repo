import React, { useEffect, useState } from "react";

interface PromptSearchBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  tags: string[];
  onTagsChange: (tags: string[]) => void;
}

export default function PromptSearchBar({
  search,
  onSearchChange,
  tags,
  onTagsChange
}: PromptSearchBarProps): JSX.Element {

  const [localSearch, setLocalSearch] = useState(search);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (localSearch !== search) {
      onSearchChange(localSearch);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [localSearch, search, onSearchChange]); // Added 'search' to the dependency array
    const [tagInput, setTagInput] = useState("");

  const addTag = (tag: string) => {
    const value = tag.trim();
    if (!value || tags.includes(value)) return;
    onTagsChange([...tags, value]);
  };

  const removeTag = (tag: string) => {
    onTagsChange(tags.filter((t) => t !== tag));
  };

  return (
    <div style={styles.container}>
      <input
        style={styles.search}
        placeholder="Search prompts by title or content..."
        value={localSearch}
        onChange={(e) => setLocalSearch(e.target.value)}
      />

            <div style={styles.tagsWrapper}>
        {tags.map((tag) => (
          <span key={tag} style={styles.tagChip}>
            {tag}
            <button
              style={styles.tagRemove}
              onClick={() => removeTag(tag)}
            >
              ×
            </button>
          </span>
        ))}
        <input
          style={styles.tagInput}
          placeholder="Add tag"
          value={tagInput}
          onChange={(e) => setTagInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              addTag(tagInput);
              setTagInput("");
            }
          }}
        />
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    gap: "10px",
    marginBottom: "12px"
  },
  search: {
    flex: 2,
    padding: "8px",
    borderRadius: "6px",
    border: "1px solid #E5E7EB"
  },
    tagsWrapper: {
    flex: 1,
    display: "flex",
    flexWrap: "wrap",
    gap: "6px",
    padding: "6px",
    borderRadius: "6px",
    border: "1px solid #E5E7EB",
    alignItems: "center"
  },
  tagChip: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
    background: "#EEF2FF",
    color: "#4F46E5",
    padding: "4px 8px",
    borderRadius: "999px",
    fontSize: "12px"
  },
  tagRemove: {
    border: "none",
    background: "transparent",
    cursor: "pointer",
    color: "#4F46E5",
    fontSize: "12px"
  },
  tagInput: {
    border: "none",
    outline: "none",
    fontSize: "13px",
    minWidth: "80px"
  }
};