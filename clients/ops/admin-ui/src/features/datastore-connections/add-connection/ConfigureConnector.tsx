import { Flex } from "@fidesui/react";
import { setStep } from "connection-type/connection-type.slice";
import React, { useState } from "react";
import { useDispatch } from "react-redux";

import Breadcrumb from "./Breadcrumb";
import ConfigurationSettingsNav from "./ConfigurationSettingsNav";
import { ConnectorParameters } from "./ConnectorParameters";
import { CONNECTOR_PARAMETERS_OPTIONS, STEPS } from "./constants";
import DatasetConfiguration from "./DatasetConfiguration";

const ConfigureConnector: React.FC = () => {
  const dispatch = useDispatch();
  const [steps, setSteps] = useState([STEPS[0], STEPS[1], STEPS[2]]);
  const [selectedItem, setSelectedItem] = useState(
    CONNECTOR_PARAMETERS_OPTIONS[0]
  );

  const handleNavChange = (value: string) => {
    switch (value) {
      case CONNECTOR_PARAMETERS_OPTIONS[1]:
        dispatch(setStep(STEPS[3]));
        setSteps([STEPS[0], STEPS[1], STEPS[3]]);
        break;
      case CONNECTOR_PARAMETERS_OPTIONS[0]:
      default:
        dispatch(setStep(STEPS[2]));
        break;
    }
    setSelectedItem(value);
  };

  return (
    <>
      <Breadcrumb steps={steps} />
      <Flex gap="18px">
        <ConfigurationSettingsNav
          onChange={handleNavChange}
          selectedItem={selectedItem}
        />
        {selectedItem === CONNECTOR_PARAMETERS_OPTIONS[0] && (
          <ConnectorParameters />
        )}
        {selectedItem === CONNECTOR_PARAMETERS_OPTIONS[1] && (
          <DatasetConfiguration />
        )}
      </Flex>
    </>
  );
};

export default ConfigureConnector;
