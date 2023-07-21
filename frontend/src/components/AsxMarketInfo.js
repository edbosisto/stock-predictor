import React, { useState, useEffect } from "react";
import MarketInfo from "./MarketInfo";

function AsxMarketInfo({ symbol, previousClose }) {
  const [currentPrice, setCurrentPrice] = useState("");
  const [percentChange, setPercentChange] = useState("");

  useEffect(() => {
    if (symbol) {
      // Fetch the current price and percent change for the selected ASX stock from the backend API
      fetch(`http://localhost:5000/api/asxstock/${symbol}`)
        .then((response) => response.json())
        .then((data) => {
          setCurrentPrice(data.current_price);
          setPercentChange(data.percent_change);
        })
        .catch((error) => {
          console.log("Error fetching ASX stock data:", error);
        });
    }
  }, [symbol]);

  return (
    <>
      <MarketInfo
        title={symbol}
        value={currentPrice}
        change={percentChange}
        previousClose={previousClose}
      />
    </>
  );
}

export default AsxMarketInfo;
