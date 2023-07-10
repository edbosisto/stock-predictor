import React from "react";

function MarketInfo({ title, state, value, change }) {
  const changeClass = change > 0 ? "positive" : "negative";
  const stateClass = state === "Open" ? "open" : "closed";

  return (
    <div className="market-info">
      <h2>{title}</h2>
      <p className={`state ${stateClass}`}>{state}</p>
      <p>{value}</p>
      <p className={`change ${changeClass}`}>{change}%</p>
    </div>
  );
}

export default MarketInfo;
