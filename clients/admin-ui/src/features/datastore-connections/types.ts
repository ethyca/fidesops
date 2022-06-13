import { Badge } from '@fidesui/react';
import { ComponentProps } from 'react';

import { PrivacyRequestStatus } from '../privacy-requests/types';

export const statusPropMap: {
  [key in PrivacyRequestStatus]: ComponentProps<typeof Badge>;
} = {
  approved: {
    bg: 'yellow.500',
    label: 'Approved',
  },
  complete: {
    bg: 'green.500',
    label: 'Completed',
  },
  denied: {
    bg: 'red.500',
    label: 'Denied',
  },
  error: {
    bg: 'red.800',
    label: 'Error',
  },
  in_processing: {
    bg: 'orange.500',
    label: 'In Progress',
  },
  paused: {
    bg: 'gray.400',
    label: 'Paused',
  },
  pending: {
    bg: 'blue.400',
    label: 'New',
  },
};

export enum ConnectionType {
  POSTGRES = 'postgres',
  MONGODB = 'mongodb',
  MYSQL = 'mysql',
  HTTPS = 'https',
  SAAS = 'saas',
  REDSHIFT = 'redshift',
  SNOWFLAKE = 'snowflake',
  MSSQL = 'mssql',
  MARIADB = 'mariadb',
  BIGQUERY = 'bigquery',
  MANUAL = 'manual',
}

export enum AccessLevel {
  READ = 'read',
  WRITE = 'write',
}

export type DatastoreConnection = {
  name: string;
  key: string;
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
  id: '',
  from: '',
  to: '',
  page: 1,
  size: 20,
};

export enum ConnectionTestStatus {
  SUCCEEDED = 'succeeded',
  FAILED = 'failed',
  SKIPPED = 'skipped',
}

export type DatastoreConnectionStatus = {
  msg: string;
  test_status?: ConnectionTestStatus;
  failure_reason?: string;
};
