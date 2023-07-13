import React, { useState, useEffect } from "react";
import styled from "styled-components";
import MarketInfo from "./MarketInfo";
import Sp500MarketInfo from "./sp500MarketInfo";

const MarketDisplayContainer = styled.div`
  display: flex;
  justify-content: space-between;
  margin: 2rem;
`;

const MarketDisplaySection = styled.div`
  width: 50%;
  padding: 1rem;
  background-color: #1e1e1e;
  display: flex;
  flex-direction: column;
  align-items: center;

  h2 {
    color: #ffffff;
    background-color: #313131;
    padding: 0.5rem;
    margin-bottom: 1rem;
    border-radius: 5px;
    cursor: pointer;

    &:hover {
      background-color: #424242;
    }
  }
`;

const DropdownMenu = styled.select`
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1rem;
`;

function MarketDisplay() {
  const [asxStocks, setAsxStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState("");

  useEffect(() => {
    // Fetch the list of ASX stocks from the backend API
    fetch("http://localhost:5000/api/asxstocks")
      .then((response) => response.json())
      .then((data) => {
        setAsxStocks(data);
      })
      .catch((error) => {
        console.log("Error fetching ASX stocks:", error);
      });
  }, []);

  const handleStockSelection = (event) => {
    setSelectedStock(event.target.value);
  };

  return (
    <MarketDisplayContainer>
      <MarketDisplaySection>
        <h2>US Index</h2>
        <Sp500MarketInfo />
      </MarketDisplaySection>
      <MarketDisplaySection>
        <h2>
          <DropdownMenu value={selectedStock} onChange={handleStockSelection}>
            <option value="">Select ASX Stock</option>
            {asxStocks.map((stock) => (
              <option key={stock.id} value={stock.symbol}>
                {stock.name}
              </option>
            ))}
          </DropdownMenu>
        </h2>
        {selectedStock && (
          <MarketInfo
            title={selectedStock}
            state="Open"
            value="200.00"
            change="2.4"
            previousClose="180.00" // Replace with actual previous close value
          />
        )}
      </MarketDisplaySection>
    </MarketDisplayContainer>
  );
}

export default MarketDisplay;
