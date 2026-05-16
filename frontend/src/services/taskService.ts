/**
 * Task Service
 * Handles task-related API operations
 */

import api from './api';
import { Task, TaskCreate, TaskUpdate, TaskFilter } from '@/types/task';

export const taskService = {
  /**
   * Get all tasks with optional filters
   */
  async getTasks(filters?: TaskFilter): Promise<Task[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      if (filters.status) params.append('status', filters.status);
      if (filters.priority) params.append('priority', filters.priority);
      if (filters.assignee_id) params.append('assignee_id', filters.assignee_id.toString());
      if (filters.team_id) params.append('team_id', filters.team_id.toString());
      if (filters.search) params.append('search', filters.search);
      if (filters.skip !== undefined) params.append('skip', filters.skip.toString());
      if (filters.limit !== undefined) params.append('limit', filters.limit.toString());
    }

    const response = await api.get<Task[]>(`/api/v1/tasks/?${params.toString()}`);
    return response.data;
  },

  /**
   * Get a single task by ID
   */
  async getTask(taskId: number): Promise<Task> {
    const response = await api.get<Task>(`/api/v1/tasks/${taskId}`);
    return response.data;
  },

  /**
   * Create a new task
   */
  async createTask(taskData: TaskCreate): Promise<Task> {
    const response = await api.post<Task>('/api/v1/tasks/', taskData);
    return response.data;
  },

  /**
   * Update an existing task
   */
  async updateTask(taskId: number, taskData: TaskUpdate): Promise<Task> {
    const response = await api.put<Task>(`/api/v1/tasks/${taskId}`, taskData);
    return response.data;
  },

  /**
   * Delete a task
   */
  async deleteTask(taskId: number): Promise<void> {
    await api.delete(`/api/v1/tasks/${taskId}`);
  },
};

// Made with Bob
