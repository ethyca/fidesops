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
  description: string;
}

export const userPrivilegesArray: UserPrivileges[] = [
  {
    privilege: 'View subject requests',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Approve subject requests',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'View datastore connections',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Manage datastore connections',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'View policies',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Create policies',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Create users',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Create roles',
    description: 'Instructional line about these particular user preferences',
  },
];