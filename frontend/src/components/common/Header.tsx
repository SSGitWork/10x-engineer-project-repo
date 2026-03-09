import React from "react";
import { NavLink, Link } from "react-router-dom"; // Updated import to include Link
import { useHealthCheck } from "../../hooks/useHealthCheck";

export default function Header(): JSX.Element {
  const { data, isError } = useHealthCheck();

  const online = data?.status === "healthy" && !isError;

  return (
    <header style={styles.header}>
      <div style={styles.left}>
        <Link to="/" style={{ textDecoration: "none", color: "inherit" }}>
        <h2 style={styles.title}>PromptLab</h2>
        </Link>

        {/* Updated nav section based on the suggestion */}
        <nav style={styles.nav}>
          <NavLink
  to="/"
  style={({ isActive }) => ({
    ...styles.navLink,
    ...(isActive ? styles.activeNav : {})
  })}
>
  Prompts
</NavLink>
          <NavLink
  to="/collections"
  style={({ isActive }) => ({
    ...styles.navLink,
    ...(isActive ? styles.activeNav : {})
  })}
>
  Collections
</NavLink> {/* Collections link */}
          <NavLink
  to="/search"
  style={({ isActive }) => ({
    ...styles.navLink,
    ...(isActive ? styles.activeNav : {})
  })}
>
  Search
</NavLink> {/* Search link */}
        </nav>
      </div>

      <div style={styles.right}>
        <span
          style={{
            ...styles.statusDot,
            backgroundColor: online ? "green" : "red",
          }}
        />
        <span>{online ? "API Online" : "API Offline"}</span>
      </div>
    </header>
  );
}

const styles: Record<string, React.CSSProperties> = {
    header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "10px",
    padding: "12px 16px",
    background: "#ffffff",
    borderBottom: "1px solid #E5E7EB",
  },
    left: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    flexWrap: "wrap",
  },
  title: {
    margin: 0,
  },
        nav: {
    display: "flex",
    gap: "8px",
    flexWrap: "wrap",
    width: "100%"
  },
  navLink: {
    textDecoration: "none",
    padding: "6px 10px",
    borderRadius: "6px",
    color: "#374151",
    fontWeight: 500
  },
  activeNav: {
    background: "#EEF2FF",
    color: "#4F46E5"
  },
    right: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
    fontSize: "12px",
  },
  statusDot: {
    width: "10px",
    height: "10px",
    borderRadius: "50%",
  },
};