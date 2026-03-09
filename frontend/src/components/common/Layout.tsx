import React from "react";
import Header from "./Header";

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps): JSX.Element {
  return (
    <div style={styles.container}>
      <Header />
      <main style={styles.main}>{children}</main>
      <footer style={styles.footer}>© 2026 PromptLab</footer>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    flexDirection: "column",
    minHeight: "100vh"
  },
  main: {
    flex: 1,
    padding: "20px"
  },
    footer: {
    textAlign: "center",
    padding: "16px",
    borderTop: "1px solid #E5E7EB",
    color: "#6B7280",
    fontSize: "14px"
  }
};