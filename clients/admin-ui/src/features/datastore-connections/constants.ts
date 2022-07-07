import { ConnectionType } from "./types";

/**
 * Relative folder path for connector images
 */
export const CONNECTOR_IMAGE_PATH = "images/connectors/";

/**
 * List of connection type image key/value pairs
 */
export const ConnectionTypeImageMap = new Map<ConnectionType, string>([
  [ConnectionType.MARIADB, "maria-db.svg"],
  [ConnectionType.MONGODB, "mongo-db.svg"],
  [ConnectionType.MSSQL, "sql-server.svg"],
  [ConnectionType.MYSQL, "my-sql.svg"],
  [ConnectionType.POSTGRES, "postgre-sql.svg"],
  [ConnectionType.REDSHIFT, "redshift.svg"],
  [ConnectionType.SNOWFLAKE, "snowflake.svg"],
]);

/**
 * Fallback connector image path if original src path doesn't exist
 */
export const FALLBACK_CONNECTOR_IMAGE_PATH = `${CONNECTOR_IMAGE_PATH}ethyca.svg`;
