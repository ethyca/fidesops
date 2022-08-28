import { useToast } from "@fidesui/react";
import { isErrorWithDetail, isErrorWithDetailArray } from "common/helpers";
import { ConnectionTypeSecretSchemaReponse } from "connection-type/types";
import { useState } from "react";

import ConnectorParametersForm from "../ConnectorParametersForm";

type ConnectorParametersProps = {
  data: ConnectionTypeSecretSchemaReponse;
  onTestConnectionClick: (value: any) => void;
};

export const ConnectorParameters: React.FC<ConnectorParametersProps> = ({
  data,
  onTestConnectionClick,
}) => {
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleError = (error: any) => {
    let errorMsg = "An unexpected error occurred. Please try again.";
    if (isErrorWithDetail(error)) {
      errorMsg = error.data.detail;
    } else if (isErrorWithDetailArray(error)) {
      errorMsg = error.data.detail[0].msg;
    }
    toast({
      status: "error",
      description: errorMsg,
    });
  };

  const handleSubmit = async (values: any) => {
    try {
      setIsSubmitting(true);
      toast({
        status: "success",
        description: "Connector successfully added!",
      });
    } catch (error) {
      handleError(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <ConnectorParametersForm
      data={data}
      isSubmitting={isSubmitting}
      onSaveClick={handleSubmit}
      onTestConnectionClick={onTestConnectionClick}
    />
  );
};
