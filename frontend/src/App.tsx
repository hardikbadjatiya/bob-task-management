/**
 * Main App Component
 * Root component with routing
 */

import { useState, useEffect } from 'react';
import { authService } from './services/authService';
import { taskService } from './services/taskService';
import { Task, TaskStatus, TaskPriority } from './types/task';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  // Add Task Modal State
  const [showAddTaskModal, setShowAddTaskModal] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState<TaskPriority>(TaskPriority.MEDIUM);
  const [newTaskStatus, setNewTaskStatus] = useState<TaskStatus>(TaskStatus.TODO);
  const [addTaskError, setAddTaskError] = useState('');

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    if (authService.isAuthenticated()) {
      try {
        await authService.getCurrentUser();
        setIsAuthenticated(true);
        await loadTasks();
      } catch (err) {
        authService.logout();
        setIsAuthenticated(false);
      }
    }
    setLoading(false);
  };

  const loadTasks = async () => {
    try {
      const data = await taskService.getTasks();
      setTasks(data);
    } catch (err) {
      console.error('Failed to load tasks:', err);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await authService.login({ email, password });
      setIsAuthenticated(true);
      await loadTasks();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setTasks([]);
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) {
      setAddTaskError('Title is required');
      return;
    }
    setAddTaskError('');
    try {
      await taskService.createTask({
        title: newTaskTitle,
        description: newTaskDescription,
        priority: newTaskPriority,
        status: newTaskStatus,
      });
      // Reset form and close modal
      setNewTaskTitle('');
      setNewTaskDescription('');
      setNewTaskPriority(TaskPriority.MEDIUM);
      setNewTaskStatus(TaskStatus.TODO);
      setShowAddTaskModal(false);
      // Reload task list
      await loadTasks();
    } catch (err: any) {
      setAddTaskError(err.response?.data?.detail || 'Failed to create task');
    }
  };

  const getStatusColor = (status: TaskStatus) => {
    switch (status) {
      case TaskStatus.TODO:
        return '#6c757d';
      case TaskStatus.IN_PROGRESS:
        return '#0d6efd';
      case TaskStatus.DONE:
        return '#198754';
      default:
        return '#6c757d';
    }
  };

  const getPriorityColor = (priority: TaskPriority) => {
    switch (priority) {
      case TaskPriority.LOW:
        return '#0dcaf0';
      case TaskPriority.MEDIUM:
        return '#ffc107';
      case TaskPriority.HIGH:
        return '#fd7e14';
      case TaskPriority.CRITICAL:
        return '#dc3545';
      default:
        return '#6c757d';
    }
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="app">
        <div className="login-container">
          <h1>Task Management System</h1>
          <form onSubmit={handleLogin} className="login-form">
            <h2>Login</h2>
            {error && <div className="error">{error}</div>}
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
            <div className="demo-credentials" style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', color: '#333', borderRadius: '5px', textAlign: 'center', fontSize: '14px', border: '1px dashed #ccc' }}>
              <p style={{ margin: '0 0 5px' }}><strong>Hackathon Demo Credentials:</strong></p>
              <p style={{ margin: 0 }}>Email: <code>demo@example.com</code></p>
              <p style={{ margin: 0 }}>Password: <code>Demo123!</code></p>
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Task Management System</h1>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </header>

      <main className="app-main">
        <div className="tasks-header">
          <h2>Tasks ({tasks.length})</h2>
          <button className="btn-primary" onClick={() => setShowAddTaskModal(true)}>+ New Task</button>
        </div>

        <div className="tasks-grid">
          {tasks.length === 0 ? (
            <div className="empty-state">
              <p>No tasks yet. Create your first task!</p>
            </div>
          ) : (
            tasks.map((task) => (
              <div key={task.id} className="task-card">
                <div className="task-header">
                  <h3>{task.title}</h3>
                  <span
                    className="task-priority"
                    style={{ backgroundColor: getPriorityColor(task.priority) }}
                  >
                    {task.priority}
                  </span>
                </div>
                {task.description && (
                  <p className="task-description">{task.description}</p>
                )}
                <div className="task-footer">
                  <span
                    className="task-status"
                    style={{ backgroundColor: getStatusColor(task.status) }}
                  >
                    {task.status.replace('_', ' ')}
                  </span>
                  <span className="task-date">
                    {new Date(task.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </main>

      {showAddTaskModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Add New Task</h2>
            <form onSubmit={handleCreateTask}>
              {addTaskError && <div className="error">{addTaskError}</div>}
              <div className="form-group">
                <label htmlFor="task-title">Title *</label>
                <input
                  id="task-title"
                  type="text"
                  placeholder="Enter task title"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="task-desc">Description</label>
                <textarea
                  id="task-desc"
                  placeholder="Enter task description"
                  value={newTaskDescription}
                  onChange={(e) => setNewTaskDescription(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="task-priority">Priority</label>
                <select
                  id="task-priority"
                  value={newTaskPriority}
                  onChange={(e) => setNewTaskPriority(e.target.value as TaskPriority)}
                >
                  {Object.values(TaskPriority).map((priority) => (
                    <option key={priority} value={priority}>
                      {priority.charAt(0).toUpperCase() + priority.slice(1)}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="task-status">Status</label>
                <select
                  id="task-status"
                  value={newTaskStatus}
                  onChange={(e) => setNewTaskStatus(e.target.value as TaskStatus)}
                >
                  {Object.values(TaskStatus).map((status) => (
                    <option key={status} value={status}>
                      {status.replace('_', ' ').charAt(0).toUpperCase() + status.replace('_', ' ').slice(1)}
                    </option>
                  ))}
                </select>
              </div>
              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => {
                    setShowAddTaskModal(false);
                    setAddTaskError('');
                  }}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Create Task
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

// Made with Bob
