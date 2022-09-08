import { Tag } from "@fidesui/react";
import React from "react";

type DaysLeftTagProps = {
  days_left: number | undefined;
  include_text: boolean;
};

const DaysLeftTag = ({ days_left, include_text }: DaysLeftTagProps) => {
  if (!days_left) {
    return null;
  }

  let backgroundColor = "";

  if (days_left >= 10) {
    backgroundColor = "green.500";
  }

  if (days_left < 10 && days_left > 4) {
    backgroundColor = "orange.500";
  }

  if (days_left < 5) {
    backgroundColor = "red.400";
  }

  const text = include_text ? `${days_left} days left` : days_left;

  return (
    <Tag backgroundColor={backgroundColor} color="white">
      {text}
    </Tag>
  );
};

export default DaysLeftTag;
