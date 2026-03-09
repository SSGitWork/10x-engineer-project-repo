import React, { useState } from "react";
import { useCreateCollection } from "../../hooks/useCollections";

export default function CollectionForm(): JSX.Element {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const createMutation = useCreateCollection();

  const resetForm = () => {
    setName("");
    setDescription("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name.trim()) {
      alert("Collection name is required");
      return;
    }

    createMutation.mutate(
      {
        name: name.trim(),
        description: description.trim() || undefined
      },
      {
        onSuccess: () => {
          resetForm();
          setOpen(false);
        }
      }
    );
  };

  return (
    <>
      <button style={styles.newButton} onClick={() => setOpen(true)}>
        New Collection
      </button>

      {open && (
        <div style={styles.overlay}>
          <div style={styles.modal}>
            <h2 style={styles.title}>New Collection</h2>

            <form onSubmit={handleSubmit} style={styles.form}>
              <label style={styles.label}>
                Name *
                <input
                  style={styles.input}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Collection name"
                />
              </label>

              <label style={styles.label}>
                Description
                <textarea
                  style={styles.textarea}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Optional description"
                />
              </label>

              <div style={styles.actions}>
                <button
                  type="button"
                  style={styles.cancelButton}
                  onClick={() => setOpen(false)}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  style={styles.createButton}
                  disabled={createMutation.isPending}
                >
                  {createMutation.isPending ? "Creating..." : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

const styles: Record<string, React.CSSProperties> = {
    newButton: {
    padding: "10px 14px",
    background: "#4F46E5",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    marginBottom: "16px",
    display: "block",
    width: "100%",
    maxWidth: "220px"
  },
  overlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    background: "rgba(0,0,0,0.4)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
    modal: {
    background: "white",
    padding: "24px",
    borderRadius: "8px",
    width: "90%",
    maxWidth: "420px",
    display: "flex",
    flexDirection: "column",
    gap: "16px"
  },
  title: {
    margin: 0
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "12px"
  },
  label: {
    display: "flex",
    flexDirection: "column",
    fontSize: "14px",
    gap: "6px"
  },
  input: {
    padding: "8px",
    borderRadius: "6px",
    border: "1px solid #E5E7EB"
  },
  textarea: {
    padding: "8px",
    borderRadius: "6px",
    border: "1px solid #E5E7EB",
    minHeight: "80px"
  },
  actions: {
    display: "flex",
    justifyContent: "flex-end",
    gap: "8px",
    marginTop: "10px"
  },
  cancelButton: {
    padding: "8px 12px",
    border: "1px solid #E5E7EB",
    background: "white",
    borderRadius: "6px",
    cursor: "pointer"
  },
  createButton: {
    padding: "8px 12px",
    background: "#4F46E5",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
  }
};