import React from "react";
import MarketInfo from "./MarketInfo";

function MarketDisplay() {
  return (
    <div className="market-display">
      <div className="left-section">
        <h2>US Index</h2>
        <MarketInfo
          title="S&P 500"
          state="Closed"
          value="3,000.00"
          change="-1.5"
        />
      </div>
      <div className="right-section">
        <h2>ASX</h2>
        <MarketInfo
          title="ASX Stock"
          state="Open"
          value="200.00"
          change="2.4"
        />
      </div>
    </div>
  );
}

export default MarketDisplay;
