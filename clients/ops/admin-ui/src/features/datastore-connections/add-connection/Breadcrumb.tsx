import {
  Box,
  Breadcrumb as ChakraBreadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
} from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { capitalize } from "common/utils";
import { selectConnectionTypeState } from "connection-type/connection-type.slice";
import { AddConnectionStep } from "connection-type/types";
import React, { useCallback } from "react";

type BreadcrumbProps = {
  steps: AddConnectionStep[];
};

const Breadcrumb: React.FC<BreadcrumbProps> = ({ steps }) => {
  const { connectionOption, step } = useAppSelector(selectConnectionTypeState);

  const getLabel = useCallback(
    (s: AddConnectionStep): string => {
      let value: string = "";
      switch (s.stepId) {
        case 2:
        case 3:
          value = s.label.replace(
            "{identifier}",
            capitalize(connectionOption!.identifier)
          );
          break;
        default:
          value = s.label;
          break;
      }
      return value;
    },
    [connectionOption]
  );

  return (
    <Box mb="16px">
      <ChakraBreadcrumb fontSize="sm" fontWeight="medium">
        {steps.map((s) => (
          <BreadcrumbItem key={s.stepId}>
            {s !== step && (
              <BreadcrumbLink href={s.href}>{getLabel(s)}</BreadcrumbLink>
            )}
            {s === step && (
              <BreadcrumbLink
                isCurrentPage
                color="complimentary.500"
                _hover={{ textDecoration: "none" }}
              >
                {getLabel(s)}
              </BreadcrumbLink>
            )}
          </BreadcrumbItem>
        ))}
      </ChakraBreadcrumb>
    </Box>
  );
};

export default Breadcrumb;
