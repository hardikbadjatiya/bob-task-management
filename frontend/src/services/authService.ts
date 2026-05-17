/**
 * Authentication Service
 * Handles user authentication operations
 */

import api from './api';
import { User, UserCreate, UserLogin } from '@/types/user';
import { Token } from '@/types/api';

export const authService = {
  /**
   * Register a new user
   */
  async register(userData: UserCreate): Promise<User> {
    const response = await api.post<User>('/auth/register', userData);
    return response.data;
  },

  /**
   * Login with email and password
   */
  async login(credentials: UserLogin): Promise<Token> {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await api.post<Token>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    return response.data;
  },

  /**
   * Logout user
   */
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me');
    return response.data;
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<Token> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post<Token>('/auth/refresh', {
      refresh_token: refreshToken,
    });

    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    return response.data;
  },
};

// Made with Bob
