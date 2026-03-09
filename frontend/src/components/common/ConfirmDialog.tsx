import React from "react";

interface ConfirmDialogProps {
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}

export default function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  onConfirm,
  onCancel
}: ConfirmDialogProps): JSX.Element | null {
  if (!open) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <h3 style={styles.title}>{title}</h3>

        <p style={styles.message}>{message}</p>

        <div style={styles.actions}>
          <button style={styles.cancel} onClick={onCancel}>
            {cancelLabel}
          </button>

          <button style={styles.confirm} onClick={onConfirm}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
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
    zIndex: 9998
  },
  modal: {
    background: "white",
    padding: "24px",
    borderRadius: "8px",
    width: "380px",
    display: "flex",
    flexDirection: "column",
    gap: "14px"
  },
  title: {
    margin: 0
  },
  message: {
    margin: 0,
    color: "#374151"
  },
  actions: {
    display: "flex",
    justifyContent: "flex-end",
    gap: "8px",
    marginTop: "10px"
  },
  cancel: {
    padding: "6px 12px",
    border: "1px solid #E5E7EB",
    borderRadius: "6px",
    background: "white",
    cursor: "pointer"
  },
  confirm: {
    padding: "6px 12px",
    border: "none",
    borderRadius: "6px",
    background: "#DC2626",
    color: "white",
    cursor: "pointer"
  }
};