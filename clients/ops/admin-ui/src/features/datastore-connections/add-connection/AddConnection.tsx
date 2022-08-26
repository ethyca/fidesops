import { Box, Heading, Text } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { capitalize } from "common/utils";
import {
  selectConnectionTypeState,
  setConnectionOption,
  setStep,
} from "connection-type/connection-type.slice";
import { AddConnectionStep } from "connection-type/types";
import ConnectionTypeLogo from "datastore-connections/ConnectionTypeLogo";
import { useRouter } from "next/router";
import React, { useCallback, useEffect } from "react";
import { useDispatch } from "react-redux";

import ChooseConnection from "./ChooseConnection";
import ConfigureConnector from "./ConfigureConnector";
import { STEPS } from "./constants";

const AddConnection: React.FC = () => {
  const dispatch = useDispatch();
  const router = useRouter();

  const { connectionOption, step } = useAppSelector(selectConnectionTypeState);

  useEffect(() => {
    if (router.query.connectorType) {
      dispatch(
        setConnectionOption(JSON.parse(router.query.connectorType as string))
      );
    } else {
      dispatch(setConnectionOption(undefined));
    }
    if (router.query.step) {
      const item = STEPS.find((s) => s.stepId === Number(router.query.step));
      dispatch(setStep(item || STEPS[1]));
    }
  }, [dispatch, router.query.connectorType, router.query.step]);

  const getComponent = useCallback(() => {
    switch (step.stepId) {
      case 1:
        return <ChooseConnection />;
      case 2:
      case 3:
        return <ConfigureConnector />;
      default:
        return <ChooseConnection />;
    }
  }, [step]);

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
    <>
      <Heading
        fontSize="2xl"
        fontWeight="semibold"
        maxHeight="40px"
        mb="4px"
        whiteSpace="nowrap"
      >
        <Box alignItems="center" display="flex">
          {connectionOption && (
            <>
              <ConnectionTypeLogo data={connectionOption.identifier} />
              <Text ml="8px">{getLabel(step)}</Text>
            </>
          )}
          {!connectionOption && <Text>{getLabel(step)}</Text>}
        </Box>
      </Heading>
      {getComponent()}
    </>
  );
};

export default AddConnection;
