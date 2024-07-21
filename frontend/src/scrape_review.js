// src/ScrapeReview.js
import React, { useState } from "react";
import { PieChart } from "@mui/x-charts/PieChart";
import axios from "axios";

const ScrapeReview = () => {
  const [productName, setProductName] = useState("");
  const [summary, setSummary] = useState(null);
  const [wordcloudImage, setWordcloudImage] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [positive, setpos] = useState(null);
  const [negative, setneg] = useState(null);
  const [neutral, setneu] = useState(null);

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post("http://127.0.0.1:5000/scrape-review", {
        product_name: productName,
      });
      const summaryData = response.statusText;
      const [neg, neu, pos] = response.data;
      setSummary(summaryData);
      setpos(pos);
      setneg(neg);
      setneu(neu);

      setWordcloudImage(`http://127.0.0.1:5000/static/${productName}.png`);
    } catch (err) {
      setError(
        "Error: " + (err.response ? err.response.data.error : err.message)
      );
    } finally {
      setLoading(false);
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
        <button type="submit">
          {loading ? "loading..." : "Scrape Reviews"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {positive && (
        <div>
          <h2>Summary</h2>
          <div className="summary">
            <p>{summary}</p>
          </div>
          <h2>Sentimental analysis</h2>
          <div
            style={{
              backgroundColor: "#f0f0f0",
              padding: "20px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              width: "fit-content",
              margin: "0 auto",
            }}
          >
            <PieChart
              colors={["red", "blue", "green"]} // Use palette
              series={[
                {
                  data: [
                    {
                      id: 0,
                      value: positive,
                      color: "blue",
                      label: "postive",
                    },
                    {
                      id: 1,
                      value: neutral,
                      color: "green",
                      label: "neutral",
                    },
                    {
                      id: 2,
                      value: negative,
                      color: "red",
                      label: "negative",
                    },
                  ],
                },
              ]}
              width={400}
              height={200}
            />
          </div>
          <h2>Word Cloud</h2>
          <img src={wordcloudImage} alt="Word Cloud" />
        </div>
      )}
    </div>
  );
};

export default ScrapeReview;
