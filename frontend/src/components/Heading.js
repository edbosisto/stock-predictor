import React from "react";

function Heading({ text }) {
  return (
    <h1
      style={{
        textAlign: "center",
        fontSize: "2.5rem",
        fontFamily: "Arial",
        marginTop: "3rem",
      }}
    >
      {text}
    </h1>
  );
}

export default Heading;
