/**
 * API Types
 * Type definitions for API responses and requests
 */

export interface ApiError {
  detail: string;
  status_code?: number;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// Made with Bob
