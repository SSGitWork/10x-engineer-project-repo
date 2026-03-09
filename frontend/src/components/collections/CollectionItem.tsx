import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Collection } from "../../api/collections";
import { useDeleteCollection } from "../../hooks/useCollections";
import ConfirmDialog from "../common/ConfirmDialog";
import { useToast } from "../common/ToastProvider";

interface CollectionItemProps {
  collection: Collection & { prompt_count?: number };
}

export default function CollectionItem({ collection }: CollectionItemProps): JSX.Element {
  const navigate = useNavigate();
  const deleteMutation = useDeleteCollection();
  const [confirmOpen, setConfirmOpen] = useState(false);
  const toast = useToast();

  const handleView = () => {
    navigate(`/collections/${collection.id}`);
  };

  const confirmDelete = () => {
    deleteMutation.mutate(collection.id, {
      onSuccess: () => {
        toast.success("Collection deleted");
        setConfirmOpen(false);
      },
      onError: () => toast.error("Failed to delete collection")
    });
  };

  return (
    <div style={styles.card}>
      <div style={styles.header}>

        <div style={styles.left}>
          <h3 style={styles.title}>{collection.name}</h3>

          
        </div>

        <div style={styles.actions}>
          <button style={styles.viewButton} onClick={handleView}>
            View
          </button>

          <button
            style={styles.deleteButton}
            onClick={() => setConfirmOpen(true)}
            disabled={deleteMutation.isPending}
          >
            Delete
          </button>
        </div>

      </div>

      {collection.description && (
        <p style={styles.description}>{collection.description}</p>
      )}

      <div style={styles.meta}>
        Created: {new Date(collection.created_at).toLocaleString()}
      </div>

      <ConfirmDialog
        open={confirmOpen}
        title="Delete Collection"
        message={`Delete collection "${collection.name}"?`}
        confirmLabel="Delete"
        onConfirm={confirmDelete}
        onCancel={() => setConfirmOpen(false)}
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
    gap: "10px"
  },

    header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "8px"
  },

  left: {
    display: "flex",
    alignItems: "center",
    gap: "12px"
  },

    title: {
    margin: 0,
    fontSize: "18px",
    wordBreak: "break-word"
  },

  

  description: {
    margin: 0,
    color: "#6B7280"
  },

  meta: {
    fontSize: "12px",
    color: "#9CA3AF"
  },

            actions: {
    display: "flex",
    gap: "8px",
    flexWrap: "wrap"
  },

        viewButton: {
    padding: "6px 10px",
    borderRadius: "6px",
    border: "1px solid #4F46E5",
    background: "#EEF2FF",
    color: "#4F46E5",
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