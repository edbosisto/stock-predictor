import React from "react";
import styled from "styled-components";
import MarketInfo from "./MarketInfo";

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

function MarketDisplay() {
  return (
    <MarketDisplayContainer>
      <MarketDisplaySection>
        <h2>US Index</h2>
        <MarketInfo
          title="S&P 500"
          state="Closed"
          value="3,000.00"
          change="-1.5"
        />
      </MarketDisplaySection>
      <MarketDisplaySection>
        <h2>ASX</h2>
        <MarketInfo
          title="ASX Stock"
          state="Open"
          value="200.00"
          change="2.4"
        />
      </MarketDisplaySection>
    </MarketDisplayContainer>
  );
}

export default MarketDisplay;
