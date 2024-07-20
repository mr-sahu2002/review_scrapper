// src/App.js
import React from "react";
import "./App.css";
import ScrapeReview from "./scrape_review";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <ScrapeReview />
      </header>
    </div>
  );
}

export default App;
