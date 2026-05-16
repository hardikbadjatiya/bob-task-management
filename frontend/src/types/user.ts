/**
 * User Types
 * Type definitions for user-related data
 */

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
  last_login: string | null;
}

export interface UserCreate {
  email: string;
  password: string;
  full_name?: string;
  avatar_url?: string;
}

export interface UserUpdate {
  full_name?: string;
  avatar_url?: string;
  password?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

// Made with Bob
