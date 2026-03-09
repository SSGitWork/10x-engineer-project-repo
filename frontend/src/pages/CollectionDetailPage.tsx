import React from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchCollection } from "../api/collections";
import { useDeleteCollection } from "../hooks/useCollections";
import PromptsList from "../components/prompts/PromptsList";
import LoadingSpinner from "../components/common/LoadingSpinner";

export default function CollectionDetailPage(): JSX.Element {
  const { collectionId } = useParams<{ collectionId: string }>();
  const navigate = useNavigate();
  const deleteMutation = useDeleteCollection();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["collection", collectionId],
    queryFn: () => fetchCollection(collectionId as string),
    enabled: !!collectionId
  });

  const handleDelete = () => {
    if (!collectionId) return;

    const confirmed = window.confirm(
      `Delete collection "${data?.name}"?\n\nAll prompts inside will also be deleted.`
    );

    if (!confirmed) return;

    deleteMutation.mutate(collectionId, {
      onSuccess: () => {
        navigate("/");
      }
    });
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError || !data) {
    return (
      <div style={styles.center}>
        <p>Failed to load collection.</p>
        <button onClick={() => refetch()}>Retry</button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.headerRow}>
        <Link to="/" style={styles.backLink}>← Back to Collections</Link>
      </div>

      <div style={styles.collectionCard}>
        <div style={styles.collectionHeader}>
          <h1 style={styles.title}>{data.name}</h1>

          <button
            style={styles.deleteButton}
            onClick={handleDelete}
            disabled={deleteMutation.isPending}
          >
            Delete Collection
          </button>
        </div>

        {data.description && (
          <p style={styles.description}>{data.description}</p>
        )}

        <div style={styles.meta}>
          Created: {new Date(data.created_at).toLocaleString()}
        </div>
      </div>

      <div style={styles.promptsSection}>
        <h2 style={styles.sectionTitle}>Prompts</h2>

        <PromptsList collectionId={collectionId as string} />
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    flexDirection: "column",
    gap: "20px"
  },
  headerRow: {
    display: "flex",
    alignItems: "center"
  },
  backLink: {
    textDecoration: "none",
    color: "#4F46E5",
    fontWeight: 500
  },
  collectionCard: {
    border: "1px solid #E5E7EB",
    borderRadius: "8px",
    padding: "20px",
    background: "#FFFFFF",
    display: "flex",
    flexDirection: "column",
    gap: "10px"
  },
  collectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center"
  },
  title: {
    margin: 0
  },
  description: {
    margin: 0,
    color: "#6B7280"
  },
  meta: {
    fontSize: "12px",
    color: "#9CA3AF"
  },
  deleteButton: {
    padding: "6px 10px",
    borderRadius: "6px",
    border: "1px solid #DC2626",
    background: "#FEE2E2",
    color: "#DC2626",
    cursor: "pointer"
  },
  promptsSection: {
    display: "flex",
    flexDirection: "column",
    gap: "10px"
  },
  sectionTitle: {
    margin: 0
  },
  center: {
    textAlign: "center",
    marginTop: "40px"
  }
};