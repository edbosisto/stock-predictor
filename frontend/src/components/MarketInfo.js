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

const MarketInfoChange = styled.p`
  color: green;

  &.negative {
    color: red;
  }
`;

function MarketInfo({ title, value, change, previousClose }) {
  const changeClass = change > 0 ? "positive" : "negative";

  return (
    <MarketInfoContainer>
      <MarketInfoTitle>{title}</MarketInfoTitle>
      <p>{value}</p>
      <MarketInfoChange className={changeClass}>
        {change}%
        <br />
        (Previous Close: {previousClose})
      </MarketInfoChange>
    </MarketInfoContainer>
  );
}

export default MarketInfo;
