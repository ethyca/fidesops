import { UserPrivileges } from './features/user-management/types';

// eslint-disable-next-line import/prefer-default-export
export const STORED_CREDENTIALS_KEY = 'auth.fidesops-admin-ui';

export const USER_PRIVILEGES: UserPrivileges[] = [
  {
    privilege: 'View subject requests',
    scope: 'privacy-request:read',
  },
  {
    privilege: 'Approve subject requests',
    scope: 'privacy-request:review',
  },
  {
    privilege: 'View datastore connections',
    scope: 'connection:read',
  },
  {
    privilege: 'Create or Update datastore connections',
    scope: 'connection:create_or_update',
  },
  {
    privilege: 'Delete datastore connections',
    scope: 'connection:delete',
  },
  {
    privilege: 'View policies',
    scope: 'policy:read',
  },
  {
    privilege: 'Create policies',
    scope: 'policy:create_or_update',
  },
  {
    privilege: 'View users',
    scope: 'user:read',
  },
  {
    privilege: 'Create users',
    scope: 'user:create',
  },
  {
    privilege: 'Create roles',
    scope: 'user-permission:create',
  },
  {
    privilege: 'View roles',
    scope: 'user-permission:read',
  },
];
