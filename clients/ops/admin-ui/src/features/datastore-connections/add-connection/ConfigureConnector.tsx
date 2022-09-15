import { Flex } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import {
  selectConnectionTypeState,
  setConnection,
  setStep
} from "connection-type/connection-type.slice";
import React, { useEffect, useRef, useState } from "react";
import { useDispatch } from "react-redux";

import Breadcrumb from "./Breadcrumb";
import ConfigurationSettingsNav from "./ConfigurationSettingsNav";
import { ConnectorParameters } from "./ConnectorParameters";
import {
  ConfigurationSettings,
  CONNECTOR_PARAMETERS_OPTIONS,
  STEPS
} from "./constants";
import DatasetConfiguration from "./DatasetConfiguration";
import DSRCustomization from "./manual/DSRCustomization";

const ConfigureConnector: React.FC = () => {
  const dispatch = useDispatch();
  const mounted = useRef(false);
  const { connectionOption } = useAppSelector(selectConnectionTypeState);
  const [steps, setSteps] = useState([STEPS[0], STEPS[1], STEPS[2]]);
  const connector = CONNECTOR_PARAMETERS_OPTIONS.find(
    (o) => o.type === connectionOption?.type
  );
  const [selectedItem, setSelectedItem] = useState(connector?.options[0]);

  const handleNavChange = (value: string) => {
    switch (value) {
      case ConfigurationSettings.DATASET_CONFIGURATION:
        dispatch(setStep(STEPS[3]));
        setSteps([STEPS[0], STEPS[1], STEPS[3]]);
        break;
      case ConfigurationSettings.DSR_CUSTOMIZATION:
        break;
      case ConfigurationSettings.CONNECTOR_PARAMETERS:
      default:
        dispatch(setStep(STEPS[2]));
        break;
    }
    setSelectedItem(value);
  };

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      dispatch(setConnection(undefined));
    };
  }, [dispatch]);

  return (
    <>
      <Breadcrumb steps={steps} />
      <Flex flex="1" gap="18px">
        <ConfigurationSettingsNav
          menuOptions={connector?.options || []}
          onChange={handleNavChange}
          selectedItem={selectedItem || ""}
        />
        {(() => {
          switch (selectedItem || "") {
            case ConfigurationSettings.CONNECTOR_PARAMETERS:
              return <ConnectorParameters />;
            case ConfigurationSettings.DATASET_CONFIGURATION:
              return <DatasetConfiguration />;
            case ConfigurationSettings.DSR_CUSTOMIZATION:
              return <DSRCustomization />;
            default:
              return null;
          }
        })()}
      </Flex>
    </>
  );
};

export default ConfigureConnector;
