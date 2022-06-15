export enum ConnectionType {
  POSTGRES = "postgres",
  MONGODB = "mongodb",
  MYSQL = "mysql",
  HTTPS = "https",
  SAAS = "saas",
  REDSHIFT = "redshift",
  SNOWFLAKE = "snowflake",
  MSSQL = "mssql",
  MARIADB = "mariadb",
  BIGQUERY = "bigquery",
  MANUAL = "manual",
}

export enum AccessLevel {
  READ = "read",
  WRITE = "write",
}

export type DatastoreConnection = {
  name: string;
  key: string;
  disabled: boolean;
  connection_type: ConnectionType;
  access: AccessLevel;
  created_at: string;
  updated_at?: string;
  last_test_timestamp?: string;
  last_test_succeeded?: boolean;
};

export type DatastoreConnectionResponse = {
  items: DatastoreConnection[];
  total: number;
  page: number;
  size: number;
};

export type DatastoreConnectionParams = {
  id: string;
  from: string;
  to: string;
  page: number;
  size: number;
  verbose?: boolean;
};

export const temp: DatastoreConnectionParams = {
  id: "",
  from: "",
  to: "",
  page: 1,
  size: 20,
};

export enum ConnectionTestStatus {
  SUCCEEDED = "succeeded",
  FAILED = "failed",
  SKIPPED = "skipped",
}

export type DatastoreConnectionStatus = {
  msg: string;
  test_status?: ConnectionTestStatus;
  failure_reason?: string;
};
