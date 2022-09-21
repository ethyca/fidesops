import { Field } from "datastore-connections/add-connection/manual/types";

export type ManualInputData = {
  checked: boolean;
  key: string;
  fields: Field;
};
