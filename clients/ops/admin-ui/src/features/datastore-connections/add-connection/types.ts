export type AddConnectionStep = {
  stepId: number;
  label: string;
  href: string;
  description?: string;
  parentStepId?: number;
};

export type CustomFields = {
  name: string;
  connectionIdentifier: string;
  description?: string;
  [key: string]: any;
};
