import { Box, Center, Heading, Spinner, Text } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { capitalize } from "common/utils";
import {
  selectConnectionTypeState,
  setConnectionOption,
  setStep,
} from "connection-type/connection-type.slice";
import { AddConnectionStep } from "connection-type/types";
import ConnectionTypeLogo from "datastore-connections/ConnectionTypeLogo";
import { useGetDatastoreConnectionByKeyQuery } from "datastore-connections/datastore-connection.slice";
import { useRouter } from "next/router";
import React, { useCallback, useEffect, useState } from "react";
import { batch, useDispatch } from "react-redux";

import ChooseConnection from "./ChooseConnection";
import ConfigureConnector from "./ConfigureConnector";
import { STEPS } from "./constants";

const AddConnection: React.FC = () => {
  const dispatch = useDispatch();
  const router = useRouter();
  const [connectionKey, setConnectionKey] = useState("");
  const [isReloading, setIsReloading] = useState(false);
  const { connectorType, key, step: currentStep } = router.query;

  const { connection, connectionOption, step } = useAppSelector(
    selectConnectionTypeState
  );
  const { data, isSuccess } = useGetDatastoreConnectionByKeyQuery(
    connectionKey,
    { skip: !connectionKey }
  );

  const reload = useCallback(() => {
    if (
      key &&
      currentStep &&
      (currentStep as unknown as number) !== step?.stepId
    ) {
      batch(() => {
        setIsReloading(true);
        setConnectionKey(key as string);
      });
    }
  }, [currentStep, key, step?.stepId]);

  useEffect(() => {
    reload();
    if (connectorType) {
      dispatch(setConnectionOption(JSON.parse(connectorType as string)));
    }
    if (router.query.step) {
      const item = STEPS.find((s) => s.stepId === Number(currentStep));
      dispatch(setStep(item || STEPS[1]));
    }
    return () => {};
  }, [connectorType, currentStep, dispatch, reload, router.query.step]);

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
      {!isReloading && (
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
      )}
      {!isReloading && getComponent()}
      {isReloading && (
        <Center>
          <Spinner />
        </Center>
      )}
    </>
  );
};

export default AddConnection;
