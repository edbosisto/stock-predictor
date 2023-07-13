import React, { useEffect, useState } from "react";
import MarketInfo from "./MarketInfo";

function Sp500MarketInfo() {
  const [sp500Data, setSp500Data] = useState(null);

  useEffect(() => {
    // Fetch S&P 500 data from the backend API
    fetch("http://localhost:5000/api/sp500")
      .then((response) => response.json())
      .then((data) => {
        setSp500Data(data);
      })
      .catch((error) => {
        console.log("Error fetching S&P 500 data:", error);
      });
  }, []);

  if (!sp500Data) {
    return null; // Render null or loading indicator while data is being fetched
  }

  return (
    <MarketInfo
      title="S&P 500"
      value={sp500Data.current_value}
      change={sp500Data.percent_change}
      previousClose={sp500Data.previous_close}
    />
  );
}

export default Sp500MarketInfo;
