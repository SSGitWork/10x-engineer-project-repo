import React from "react";
import PromptsList from "../components/prompts/PromptsList";

export default function PromptsPage(): JSX.Element {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Prompts</h1>

      <PromptsList />
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
  }
};