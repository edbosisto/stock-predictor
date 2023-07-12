import React from "react";
import styled from "styled-components";

const HeadingContainer = styled.h1`
  text-align: center;
  font-size: 2.5rem;
  font-family: Arial;
  margin-top: 3rem;
`;

function Heading({ text }) {
  return <HeadingContainer>{text}</HeadingContainer>;
}

export default Heading;
