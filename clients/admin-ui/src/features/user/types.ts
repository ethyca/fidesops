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
  search: string;
}

export interface UserResponse {
  name: string;
  username: string;
  password: string;
  id: string;
}

export interface UserParams {
  id: string;
}
