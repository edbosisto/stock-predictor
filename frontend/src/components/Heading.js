import React from "react";

function Heading({ text }) {
  const headingStyles = {
    textAlign: "center",
    fontSize: "2.5rem",
    fontFamily: "Arial",
    marginTop: "3rem",
  };

  return <h1 style={headingStyles}>{text}</h1>;
}

export default Heading;
