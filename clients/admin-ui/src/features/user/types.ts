export interface User {
  id?: string;
  name?: string;
  username?: string;
  password?: string;
}

export interface UserResponse {
  id: string;
}

export interface UsersListParams {
  page: number;
  size: number;
  user: User;
}

export interface UsersResponse {
  items: User[];
  total: number;
}

export interface UserPrivileges {
  privilege: string;
  scopes: string[];
}

export interface UserPermissions {
  scopes: string[];
  id?: string;
}

export const userPrivilegesArray: UserPrivileges[] = [
  {
    privilege: 'View subject requests',
    scopes: ['privacy-request:read'],
  },
  {
    privilege: 'Approve subject requests',
    scopes: ['privacy-request:administrate:approve'],
  },
  {
    privilege: 'View datastore connections',
    scopes: ['connection:read'],
  },
  {
    privilege: 'Manage datastore connections',
    scopes: [
      'connection:read',
      'connection:create_or_update',
      'connection:delete',
    ],
  },
  {
    privilege: 'View policies',
    scopes: ['policy:read'],
  },
  {
    privilege: 'Create policies',
    scopes: ['policy:create_or_update'],
  },
  {
    privilege: 'Create users',
    scopes: ['user:create'],
  },
  {
    privilege: 'Create roles',
    scopes: ['role:create'],
  },
];
