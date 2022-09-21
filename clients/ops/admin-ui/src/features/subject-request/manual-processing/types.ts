export type ManualInputData = {
  checked: boolean;
  fields: ManualInputDataField[];
  key: string;
};

export type ManualInputDataField = {
  [key: string]: any;
};
