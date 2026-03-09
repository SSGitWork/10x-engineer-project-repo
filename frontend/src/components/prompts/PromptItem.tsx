import React, { useState } from "react";
import { Prompt } from "../../api/prompts";
import { useDeletePrompt } from "../../hooks/usePrompts";
import ConfirmDialog from "../common/ConfirmDialog";
import { useToast } from "../common/ToastProvider";

interface PromptItemProps {
  prompt: Prompt;
  onEdit: (prompt: Prompt) => void;
}

export default function PromptItem({ prompt, onEdit }: PromptItemProps): JSX.Element {
  const deleteMutation = useDeletePrompt();
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [hover, setHover] = useState(false);
  const toast = useToast();

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(prompt.content);
      toast.success("Prompt copied to clipboard");
    } catch {
      toast.error("Failed to copy prompt");
    }
  };

  // Create a new function for performing the delete action
  const confirmDelete = () => {
    deleteMutation.mutate(prompt.id, {
      onSuccess: () => {
        toast.success("Prompt deleted");
        setConfirmOpen(false); // Set confirmOpen to false upon successful deletion
      },
      onError: () => {
        toast.error("Failed to delete prompt");
      }
    });
  };

  // Updated handleDelete to only open confirm dialog
  const handleDelete = () => {
    setConfirmOpen(true);
  };

    return (
    <div
      style={{
        ...styles.card,
        transform: hover ? "translateY(-2px)" : "translateY(0)",
        boxShadow: hover
          ? "0 4px 12px rgba(0,0,0,0.08)"
          : "0 1px 2px rgba(0,0,0,0.04)"
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <div style={styles.header}>
        <h3 style={styles.title}>{prompt.title}</h3>

                <div style={styles.actions}>
          <button style={styles.editButton} onClick={() => onEdit(prompt)}>
            Edit
          </button>

          <button style={styles.copyButton} onClick={handleCopy}>
            Copy
          </button>

          <button
            style={styles.deleteButton}
            onClick={handleDelete}
            disabled={deleteMutation.isPending}
          >
            Delete
          </button>
        </div>
      </div>

      {prompt.description && (
        <p style={styles.description}>{prompt.description}</p>
      )}

      <p style={styles.preview}>
        {prompt.content.length > 120
          ? prompt.content.slice(0, 120) + "..."
          : prompt.content}
      </p>

      <div style={styles.tags}>
        {prompt.tags?.map((tag) => (
          <span key={tag} style={styles.tag}>
            {tag}
          </span>
        ))}
      </div>

      <div style={styles.meta}>
        Updated: {new Date(prompt.updated_at).toLocaleString()}
      </div>

      <ConfirmDialog
        open={confirmOpen} // Updated prop to 'open'
        title="Delete Prompt" // Changed the title to a static string as per the suggestion
        message={`Delete prompt "${prompt.title}"?`} // Updated message
        confirmLabel="Delete" // Added the confirmLabel prop
        onConfirm={confirmDelete} // Changed to use the new confirmDelete function
        onCancel={() => setConfirmOpen(false)} // Renamed from onClose to onCancel
      />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
    card: {
    border: "1px solid #E5E7EB",
    borderRadius: "8px",
    padding: "16px",
    background: "#FFFFFF",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    transition: "all 0.2s ease",
    boxShadow: "0 1px 2px rgba(0,0,0,0.04)"
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center"
  },
  title: {
    margin: 0,
    fontSize: "16px"
  },
    description: {
    margin: 0,
    color: "#6B7280"
  },
  preview: {
    margin: 0,
    fontSize: "13px",
    color: "#374151",
    lineHeight: 1.4
  },
  tags: {
    display: "flex",
    gap: "6px",
    flexWrap: "wrap"
  },
  tag: {
    background: "#EEF2FF",
    color: "#4F46E5",
    padding: "4px 8px",
    borderRadius: "6px",
    fontSize: "12px"
  },
  meta: {
    fontSize: "12px",
    color: "#9CA3AF"
  },
  actions: {
    display: "flex",
    gap: "6px"
  },
  editButton: {
    padding: "6px 10px",
    borderRadius: "6px",
    border: "1px solid #4F46E5",
    background: "#EEF2FF",
    color: "#4F46E5",
    cursor: "pointer"
  },
    copyButton: {
    padding: "6px 10px",
    borderRadius: "6px",
    border: "1px solid #059669",
    background: "#D1FAE5",
    color: "#065F46",
    cursor: "pointer"
  },
  deleteButton: {
    padding: "6px 10px",
    borderRadius: "6px",
    border: "1px solid #DC2626",
    background: "#FEE2E2",
    color: "#DC2626",
    cursor: "pointer"
  }
};

