// src/ScrapeReview.js
import React, { useState } from "react";
import axios from "axios";

const ScrapeReview = () => {
  const [productName, setProductName] = useState("");
  const [sentiment, setSentiment] = useState(null);
  const [summary, setSummary] = useState(null);
  const [wordcloudImage, setWordcloudImage] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post("http://127.0.0.1:5000/scrape-review", {
        product_name: productName,
      });
      const summaryData = response.statusText;
      const sentimentData = response.data;
      setSummary(summaryData);
      setSentiment(sentimentData);

      setWordcloudImage(`http://127.0.0.1:5000/static/${productName}.png`);
    } catch (err) {
      setError(
        "Error: " + (err.response ? err.response.data.error : err.message)
      );
    }
  };

  return (
    <div>
      <h1>Scrape Reviews</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="Enter product name"
          required
        />
        <button type="submit">Scrape Reviews</button>
      </form>
      {error && <p className="error">{error}</p>}
      {sentiment && (
        <div>
          <div className="summary">
            <h2>Summary</h2>
            <p>{summary}</p>
          </div>
          <div className="sentiment-analysis">
            <h2>Sentiment Analysis</h2>
            <p>{sentiment}</p>
          </div>
          <h2>Word Cloud</h2>
          <img src={wordcloudImage} alt="Word Cloud" />
        </div>
      )}
    </div>
  );
};

export default ScrapeReview;
