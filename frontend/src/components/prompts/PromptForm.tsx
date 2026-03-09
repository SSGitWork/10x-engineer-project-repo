import React, { useState, useEffect } from "react";
import { Prompt } from "../../api/prompts";
import { useCreatePrompt, useUpdatePrompt } from "../../hooks/usePrompts";
import { useCollections, useCreateCollection } from "../../hooks/useCollections";

interface PromptFormProps {
  collectionId: string;
  editingPrompt: Prompt | null;
  onClose: () => void;
}

export default function PromptForm({
  collectionId,
  editingPrompt,
  onClose
}: PromptFormProps): JSX.Element {

  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [description, setDescription] = useState("");
    const [tags, setTags] = useState("");
  const [selectedCollection, setSelectedCollection] = useState<string>(collectionId || "");
  const [showNewCollection, setShowNewCollection] = useState(false);
  const [newCollectionName, setNewCollectionName] = useState("");
  const [newCollectionDescription, setNewCollectionDescription] = useState("");

  const { data: collections } = useCollections();
  const createCollectionMutation = useCreateCollection();

  const createMutation = useCreatePrompt();
  const updateMutation = useUpdatePrompt();

  useEffect(() => {
    if (editingPrompt) {
      setOpen(true);
      setTitle(editingPrompt.title);
      setContent(editingPrompt.content);
      setDescription(editingPrompt.description || "");
      setTags(editingPrompt.tags.join(", "));
    }
  }, [editingPrompt]);

  const reset = () => {
    setTitle("");
    setContent("");
    setDescription("");
    setTags("");
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || !content.trim()) {
      alert("Title and content are required");
      return;
    }

    const parsedTags = tags
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);

    if (editingPrompt) {
      updateMutation.mutate(
        {
          id: editingPrompt.id,
          payload: {
            title,
            content,
            description,
            tags: parsedTags
          }
        },
        {
          onSuccess: () => {
            reset();
            setOpen(false);
            onClose();
          }
        }
      );
    } else {
            createMutation.mutate(
        {
          title,
          content,
          description,
          collection_id: selectedCollection || undefined,
          tags: parsedTags
        },
        {
          onSuccess: () => {
            reset();
            setOpen(false);
          }
        }
      );
    }
  };

  return (
    <>
      {!editingPrompt && (
        <button style={styles.newButton} onClick={() => setOpen(true)}>
          New Prompt
        </button>
      )}

      {open && (
        <div style={styles.overlay}>
          <div style={styles.modal}>
            <h2>{editingPrompt ? "Edit Prompt" : "New Prompt"}</h2>

            <form onSubmit={handleSubmit} style={styles.form}>

                            <label style={styles.field}>
                <span style={styles.label}>Title *</span>
                <input
                  style={styles.input}
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />
              </label>

                            <label style={styles.field}>
                <span style={styles.label}>Content *</span>
                <textarea
                  style={styles.textarea}
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                />
              </label>

                            <label style={styles.field}>
                <span style={styles.label}>Description</span>
                <input
                  style={styles.input}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </label>

                            <label style={styles.field}>
                <span style={styles.label}>Tags (comma separated)</span>
                <input
                  style={styles.input}
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                />
              </label>

              <label style={styles.field}>
                <span style={styles.label}>Collection</span>
                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                  <select
                    style={styles.input}
                    value={selectedCollection}
                    onChange={(e) => setSelectedCollection(e.target.value)}
                  >
                    <option value="">No Collection</option>
                    {(collections?.collections ?? []).map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>

                  <button
                    type="button"
                    onClick={() => setShowNewCollection(!showNewCollection)}
                  >
                    + New Collection
                  </button>
                </div>
              </label>

              {showNewCollection && (
                <div style={{ border: "1px solid #E5E7EB", padding: "12px", borderRadius: "6px" }}>
                  <label style={styles.field}>
                    <span style={styles.label}>New Collection Name *</span>
                    <input
                      style={styles.input}
                      value={newCollectionName}
                      onChange={(e) => setNewCollectionName(e.target.value)}
                    />
                  </label>

                  <label style={styles.field}>
                    <span style={styles.label}>Description</span>
                    <input
                      style={styles.input}
                      value={newCollectionDescription}
                      onChange={(e) => setNewCollectionDescription(e.target.value)}
                    />
                  </label>

                  <button
                    type="button"
                    onClick={() => {
                      if (!newCollectionName.trim()) return;

                      createCollectionMutation.mutate(
                        { name: newCollectionName, description: newCollectionDescription },
                        {
                          onSuccess: (created) => {
                            setSelectedCollection(created.id);
                            setNewCollectionName("");
                            setNewCollectionDescription("");
                            setShowNewCollection(false);
                          }
                        }
                      );
                    }}
                  >
                    Create Collection
                  </button>
                </div>
              )}

              <div style={styles.actions}>
                <button
                  type="button"
                  style={styles.cancelButton}
                  onClick={() => { setOpen(false); onClose(); }}
                >
                  Cancel
                </button>


                <button
                  type="submit"
                  style={styles.submitButton}
                >
                  {editingPrompt ? "Save Prompt" : "Create Prompt"}
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
    padding: "10px 16px",
    background: "#4F46E5",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: "14px"
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
    justifyContent: "center",
    zIndex: 2000
  },
    modal: {
    background: "white",
    padding: "28px",
    borderRadius: "10px",
    width: "520px",
    maxWidth: "90%",
    display: "flex",
    flexDirection: "column",
    gap: "14px"
  },
    form: {
    display: "flex",
    flexDirection: "column",
    gap: "16px"
  },
    field: {
    display: "flex",
    flexDirection: "column",
    gap: "6px"
  },
  label: {
    fontSize: "13px",
    fontWeight: 500,
    color: "#374151"
  },
  input: {
    padding: "10px",
    border: "1px solid #E5E7EB",
    borderRadius: "6px",
    width: "100%",
    fontSize: "14px"
  },
  textarea: {
    padding: "10px",
    border: "1px solid #E5E7EB",
    borderRadius: "6px",
    minHeight: "140px",
    width: "100%",
    fontSize: "14px",
    resize: "vertical"
  },
  actions: {
    display: "flex",
    justifyContent: "flex-end",
    gap: "12px",
    marginTop: "16px"
  },
  cancelButton: {
    border: "1px solid #E5E7EB",
    background: "#FFFFFF",
    padding: "8px 14px",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: 500
  },

  submitButton: {
    border: "none",
    background: "#4F46E5",
    color: "white",
    padding: "8px 14px",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: 500
  }
};


