/**
 * Enums
 */
export enum AccessLevel {
  READ = "read",
  WRITE = "write",
}

export enum ConnectionTestStatus {
  SUCCEEDED = "succeeded",
  FAILED = "failed",
  SKIPPED = "skipped",
}

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

export enum DisabledStatus {
  ACTIVE = "active",
  DISABLED = "disabled",
}

export enum SassType {
  MAILCHIMP = "mailchimp",
  HUB_SPOT = "hubspot",
  OUTREACH = "outreach",
  SALES_FORCE = "salesforce",
  SEGMENT = "segment",
  SENTRY = "sentry",
  STRIPE = "stripe",
  ZENDESK = "zendesk",
  CUSTOM = "custom",
}

export enum SystemType {
  SAAS = "saas",
  DATABASE = "database",
  MANUAL = "manual",
}

export enum TestingStatus {
  PASSED = "passed",
  FAILED = "failed",
  UNTESTED = "untested",
}

/**
 * Relative folder path for connector images
 */
export const CONNECTOR_IMAGE_PATH = "images/connectors/";

/**
 * List of connection type image key/value pairs
 */
export const ConnectionTypeImageMap = new Map<
  ConnectionType | SassType,
  string
>([
  [ConnectionType.MARIADB, "mariadb.svg"],
  [ConnectionType.MONGODB, "mongodb.svg"],
  [ConnectionType.MSSQL, "sqlserver.svg"],
  [ConnectionType.MYSQL, "mysql.svg"],
  [ConnectionType.POSTGRES, "postgres.svg"],
  [ConnectionType.REDSHIFT, "redshift.svg"],
  [ConnectionType.SNOWFLAKE, "snowflake.svg"],
  [SassType.HUB_SPOT, "hubspot.svg"],
  [SassType.MAILCHIMP, "mailchimp.svg"],
  [SassType.OUTREACH, "outreach.svg"],
  [SassType.SALES_FORCE, "salesforce.svg"],
  [SassType.SEGMENT, "segment.svg"],
  [SassType.SENTRY, "sentry.svg"],
  [SassType.STRIPE, "stripe.svg"],
  [SassType.ZENDESK, "zendesk.svg"],
]);

/**
 * Fallback connector image path if original src path doesn't exist
 */
export const FALLBACK_CONNECTOR_IMAGE_PATH = `${CONNECTOR_IMAGE_PATH}ethyca.svg`;
