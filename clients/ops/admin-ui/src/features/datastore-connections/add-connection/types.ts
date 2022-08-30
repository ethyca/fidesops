export type BaseConnectorParametersFields = {
  description: string;
  name: string;
  instance_key: string;
  [key: string]: any;
};

export type DatabaseConnectorParametersFormFields =
  BaseConnectorParametersFields;

export type SaasConnectorParametersFormFields = BaseConnectorParametersFields;
