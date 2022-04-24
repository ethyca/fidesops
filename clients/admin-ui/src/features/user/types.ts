export interface User {
  name: string;
  username: string;
  password: string;
  id: string;
}

export interface UsersResponse {
  users: User[];
}

export interface UsersParams {
  id: string;
  page: number;
  size: number;
}

export interface UserResponse {
  name: string;
  username: string;
  password: string;
  id: string;
}

export interface UserParams {
  user: User
}
