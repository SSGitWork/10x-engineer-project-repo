import React from "react";
import Layout from "./components/common/Layout";
import AppRouter from "./router/AppRouter";

export default function App(): JSX.Element {
  return (
    <Layout>
      <AppRouter />
    </Layout>
  );
}