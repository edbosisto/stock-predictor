import React, { useState, useEffect } from "react";
import styled from "styled-components";

const StockComparisonContainer = styled.div`
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #313131;
  padding: 1rem;
  border-radius: 5px;
`;

const ComparisonExplain = styled.h3`
  color: #ffffff;
  margin: 0;
`;

const ComparisonResult = styled.p`
  color: #ffffff;
  margin: 0;
`;

const StockComparison = ({ symbol }) => {
  const [comparisonData, setComparisonData] = useState(null);

  useEffect(() => {
    if (symbol) {
      // Fetch stock comparison data from the backend API when the symbol is available
      fetch(`http://localhost:5000/api/compare?symbol=${symbol}`)
        .then((response) => response.json())
        .then((data) => {
          setComparisonData(data);
        })
        .catch((error) => {
          console.log("Error fetching stock comparison:", error);
          setComparisonData(null); // Clear comparison data on error
        });
    } else {
      setComparisonData(null); // Clear comparison data when symbol is not selected
    }
  }, [symbol]);

  return (
    <StockComparisonContainer>
      {comparisonData ? (
        <>
          <ComparisonExplain>
            Based on the previous day's performance of the S&P 500:
          </ComparisonExplain>
          <ComparisonResult>
            Probability of {symbol} moving in the same direction today:{" "}
            {comparisonData.probability_same_direction}%
          </ComparisonResult>
          <ComparisonResult>
            Probability of {symbol} moving in the opposite direction today:{" "}
            {comparisonData.probability_opposite_direction}%
          </ComparisonResult>
        </>
      ) : null}
    </StockComparisonContainer>
  );
};

export default StockComparison;
