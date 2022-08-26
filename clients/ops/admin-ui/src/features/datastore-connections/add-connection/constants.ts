import { ItemOption } from "common/dropdown/types";
import { AddConnectionStep } from "connection-type/types";
import { SystemType } from "datastore-connections/constants";

import { DATASTORE_CONNECTION_ROUTE } from "../../../constants";

export const CONNECTION_TYPE_FILTER_MAP = new Map<string, ItemOption>([
  [
    "Database connectors",
    {
      value: SystemType.DATABASE.toString(),
    },
  ],
  ["Third party connectors", { value: SystemType.SAAS.toString() }],
  ["Show all", { value: "" }],
]);

export const CONNECTOR_PARAMETERS_OPTIONS = [
  "Connector parameters",
  "Dataset configuration",
];

export const DEFAULT_CONNECTION_TYPE_FILTER = CONNECTION_TYPE_FILTER_MAP.get(
  "Show all"
)?.value as string;

export const STEPS: AddConnectionStep[] = [
  {
    stepId: 0,
    label: "Datastore Connections",
    href: DATASTORE_CONNECTION_ROUTE,
  },
  {
    stepId: 1,
    label: "Choose your connection",
    href: `${DATASTORE_CONNECTION_ROUTE}/new?step=1`,
    description:
      "The building blocks of your data map are the list of systems that exist in your organization. Think of systems as as anything that might store or process data in your organization, from a web application, to a database, or data warehouse.",
    parentStepId: 0,
  },
  {
    stepId: 2,
    label: "Configure your {identifier} connection",
    description:
      "Connect to your {identifier} environment by providing credential information below. Once you have saved your connector credentials, you can review what data is included when processing a privacy request in your Dataset configuration.",
    href: `${DATASTORE_CONNECTION_ROUTE}/new?step=2`,
    parentStepId: 1,
  },
  {
    stepId: 3,
    label: "Configure your {identifier} connection",
    description:
      "View your system yaml below! You can also modify the yaml if you need to assign any references between datasets.",
    href: `${DATASTORE_CONNECTION_ROUTE}/new?step=3`,
    parentStepId: 1,
  },
];
