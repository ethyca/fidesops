export interface User {
  id: string;
  name?: string;
  username?: string;
  password?: string;
}

export interface UserResponse {
  id: string;
}

export interface UsersParams {
  page: number;
  size: number;
}

export interface UsersResponse {
  users: User[];
}
