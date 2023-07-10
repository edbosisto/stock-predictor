import React from "react";
import styled from "styled-components";

const MarketInfoContainer = styled.div`
  margin-top: 1rem;
  text-align: center;
`;

const MarketInfoTitle = styled.h2`
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
`;

const MarketInfoState = styled.p`
  font-weight: bold;

  &.open {
    color: #32cd32;
  }

  &.closed {
    color: #ff0000;
  }
`;

const MarketInfoChange = styled.p`
  color: green;

  &.negative {
    color: red;
  }
`;

function MarketInfo({ title, state, value, change }) {
  const changeClass = change > 0 ? "positive" : "negative";
  const stateClass = state === "Open" ? "open" : "closed";

  return (
    <MarketInfoContainer>
      <MarketInfoTitle>{title}</MarketInfoTitle>
      <MarketInfoState className={stateClass}>{state}</MarketInfoState>
      <p>{value}</p>
      <MarketInfoChange className={changeClass}>{change}%</MarketInfoChange>
    </MarketInfoContainer>
  );
}

export default MarketInfo;
