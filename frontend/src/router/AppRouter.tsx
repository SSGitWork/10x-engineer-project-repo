import React from "react";
import { Routes, Route } from "react-router-dom";
import PromptsPage from "../pages/PromptsPage";
import CollectionDetailPage from "../pages/CollectionDetailPage";
import GlobalSearchPage from "../pages/GlobalSearchPage";
import CollectionsPage from "../pages/CollectionsPage";

export default function AppRouter(): JSX.Element {
  return (
    <Routes>
      <Route path="/" element={<PromptsPage />} />
      <Route path="/collections/:collectionId" element={<CollectionDetailPage />} />
      <Route path="/collections" element={<CollectionsPage />} /> {/* Added collections route */}
      <Route path="/search" element={<GlobalSearchPage />} />
    </Routes>
  );
}