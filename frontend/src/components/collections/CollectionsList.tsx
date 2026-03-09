import React from "react";
import { useCollections } from "../../hooks/useCollections";
import CollectionItem from "./CollectionItem";
import LoadingSpinner from "../common/LoadingSpinner";

export default function CollectionsList(): JSX.Element {
  const { data, isLoading, isError, refetch } = useCollections();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError) {
    return (
      <div style={styles.center}>
        <p>Failed to load collections.</p>
        <button onClick={() => refetch()}>Retry</button>
      </div>
    );
  }

  const collections = data?.collections ?? [];

  if (collections.length === 0) {
    return (
      <div style={styles.center}>
        <p>No collections yet.</p>
        <p>Create your first collection to get started.</p>
      </div>
    );
  }

  return (
    <div style={styles.grid}>
      {collections.map((collection) => (
        <CollectionItem key={collection.id} collection={collection} />
      ))}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  grid: {
    display: "flex",
    flexDirection: "column",
    gap: "12px"
  },
  center: {
    textAlign: "center",
    marginTop: "40px"
  }
};