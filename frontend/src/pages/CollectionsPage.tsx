import React from "react";
import CollectionsList from "../components/collections/CollectionsList";
import CollectionForm from "../components/collections/CollectionForm";

export default function CollectionsPage(): JSX.Element {
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <h1>Collections</h1>
        <CollectionForm />
    </div>

      <CollectionsList />
    </div>
  );
}