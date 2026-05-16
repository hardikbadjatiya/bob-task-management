# 🧪 Testing Guide - Task Management System

## Overview

This guide provides comprehensive instructions for testing the Task Management System application, including startup procedures, API testing, and validation steps.

---

## 📋 Prerequisites

### For Docker Setup (Recommended)
- Docker Desktop installed and running
- Docker Compose v2.0+
- 8GB RAM minimum
- Ports 3000, 5432, 6379, 8000 available

### For Local Development Setup
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- npm or yarn

---

## 🚀 Quick Start

### Option 1: Docker Setup (Recommended)

```bash
# 1. Start Docker Desktop

# 2. Run the startup script
./start.sh

# 3. Wait for services to be ready (30-60 seconds)

# 4. Access the application
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development Setup

```bash
# 1. Ensure PostgreSQL and Redis are running

# 2. Run the development startup script
./start-dev.sh

# 3. Access the application
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🧪 Running Tests

### Automated Test Suite

Once the application is running, execute the test script:

```bash
./test.sh
```

This will test:
- ✅ Backend API health
- ✅ API documentation endpoints
- ✅ Authentication endpoints
- ✅ Task management endpoints
- ✅ User management endpoints
- ✅ Team management endpoints
- ✅ Frontend accessibility

### Expected Test Results

```
🧪 Testing Task Management System...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Backend API Tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Testing Backend Root... ✅ PASSED (HTTP 200)
Testing API Docs... ✅ PASSED (HTTP 200)
Testing OpenAPI Schema... ✅ PASSED (HTTP 200)

🔐 Authentication Endpoints

Testing Register Endpoint... ✅ PASSED (HTTP 422)
Testing Login Endpoint... ✅ PASSED (HTTP 422)

📝 Task Endpoints (Unauthorized)

Testing Get Tasks (Unauthorized)... ✅ PASSED (HTTP 401)

👥 User Endpoints (Unauthorized)

Testing Get Current User (Unauthorized)... ✅ PASSED (HTTP 401)

🏢 Team Endpoints (Unauthorized)

Testing Get Teams (Unauthorized)... ✅ PASSED (HTTP 401)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Frontend Tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Testing Frontend Root... ✅ PASSED (HTTP 200)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Test Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests Passed: 10
Tests Failed: 0
Total Tests:  10

🎉 All tests passed!
```

---

## 🔍 Manual Testing Procedures

### 1. Backend API Testing

#### Test 1: Health Check
```bash
curl http://localhost:8000/
```
**Expected Response:**
```json
{
  "message": "Task Management API",
  "version": "1.0.0",
  "status": "healthy"
}
```

#### Test 2: API Documentation
Visit: http://localhost:8000/docs

**Expected:** Interactive Swagger UI with all API endpoints

#### Test 3: User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "created_at": "2026-05-16T07:00:00Z"
}
```

#### Test 4: User Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Test 5: Create Task (Authenticated)
```bash
# Save the access_token from login response
TOKEN="your_access_token_here"

curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Test Task",
    "description": "This is a test task",
    "priority": "high",
    "status": "todo"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "title": "Test Task",
  "description": "This is a test task",
  "priority": "high",
  "status": "todo",
  "created_at": "2026-05-16T07:00:00Z",
  "updated_at": "2026-05-16T07:00:00Z"
}
```

#### Test 6: Get All Tasks
```bash
curl -X GET http://localhost:8000/api/v1/tasks/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Test Task",
      "description": "This is a test task",
      "priority": "high",
      "status": "todo"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

### 2. Frontend Testing

#### Test 1: Access Frontend
Visit: http://localhost:3000

**Expected:** Login page with email and password fields

#### Test 2: User Registration Flow
1. Click "Register" or "Sign Up"
2. Fill in:
   - Email: test@example.com
   - Password: SecurePass123!
   - Full Name: Test User
3. Click "Register"

**Expected:** Redirect to login page or dashboard

#### Test 3: User Login Flow
1. Enter credentials:
   - Email: test@example.com
   - Password: SecurePass123!
2. Click "Login"

**Expected:** Redirect to task dashboard

#### Test 4: Task Management
1. Click "Create Task" or "Add Task"
2. Fill in task details:
   - Title: My First Task
   - Description: Testing task creation
   - Priority: High
   - Status: To Do
3. Click "Save"

**Expected:** Task appears in the task list

#### Test 5: Task Filtering
1. Use filter dropdowns to filter by:
   - Status (Todo, In Progress, Done)
   - Priority (Low, Medium, High)

**Expected:** Task list updates based on filters

---

## 🐛 Troubleshooting

### Issue: Docker containers won't start

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove volumes
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

### Issue: Port already in use

**Solution:**
```bash
# Check what's using the port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Kill the process or change ports in docker-compose.yml
```

### Issue: Backend database connection error

**Solution:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Issue: Frontend can't connect to backend

**Solution:**
1. Check backend is running: `curl http://localhost:8000/`
2. Check CORS settings in `backend/app/config.py`
3. Verify `VITE_API_URL` in frontend environment

### Issue: Authentication not working

**Solution:**
1. Check SECRET_KEY is set in `backend/.env`
2. Verify token expiration settings
3. Clear browser cookies and local storage
4. Check backend logs: `docker-compose logs backend`

---

## 📊 Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench
# macOS: brew install httpd
# Ubuntu: sudo apt-get install apache2-utils

# Test backend health endpoint
ab -n 1000 -c 10 http://localhost:8000/

# Test with authentication
ab -n 100 -c 5 -H "Authorization: Bearer YOUR_TOKEN" \
   http://localhost:8000/api/v1/tasks/
```

### Expected Performance Metrics
- **Response Time**: < 100ms for simple queries
- **Throughput**: > 100 requests/second
- **Error Rate**: < 1%

---

## 🔒 Security Testing

### Test 1: SQL Injection Prevention
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com OR 1=1--",
    "password": "anything"
  }'
```
**Expected:** 401 Unauthorized (not vulnerable)

### Test 2: XSS Prevention
```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "<script>alert(\"XSS\")</script>",
    "description": "Test"
  }'
```
**Expected:** Script tags should be escaped in response

### Test 3: Authentication Required
```bash
curl -X GET http://localhost:8000/api/v1/tasks/
```
**Expected:** 401 Unauthorized

---

## 📈 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f redis

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Check Service Status

```bash
# List all containers
docker-compose ps

# Check health
docker-compose ps | grep healthy
```

### Database Inspection

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U taskuser -d taskdb

# List tables
\dt

# Query users
SELECT * FROM users;

# Query tasks
SELECT * FROM tasks;

# Exit
\q
```

---

## ✅ Test Checklist

### Backend Tests
- [ ] Health endpoint responds
- [ ] API documentation accessible
- [ ] User registration works
- [ ] User login returns JWT token
- [ ] Protected endpoints require authentication
- [ ] Task CRUD operations work
- [ ] User CRUD operations work
- [ ] Team CRUD operations work
- [ ] Input validation works
- [ ] Error handling works

### Frontend Tests
- [ ] Application loads
- [ ] Login page displays
- [ ] Registration works
- [ ] Login works
- [ ] Task list displays
- [ ] Task creation works
- [ ] Task editing works
- [ ] Task deletion works
- [ ] Filtering works
- [ ] Logout works

### Integration Tests
- [ ] Frontend can communicate with backend
- [ ] Authentication flow works end-to-end
- [ ] Task management flow works end-to-end
- [ ] Team collaboration works
- [ ] Real-time updates work (if implemented)

### Security Tests
- [ ] SQL injection prevented
- [ ] XSS attacks prevented
- [ ] CSRF protection enabled
- [ ] Authentication required for protected routes
- [ ] Password hashing works
- [ ] JWT tokens expire correctly

### Performance Tests
- [ ] Response times acceptable
- [ ] Concurrent users supported
- [ ] Database queries optimized
- [ ] Caching works (Redis)

---

## 🎯 Success Criteria

The application passes testing if:

1. ✅ All automated tests pass (10/10)
2. ✅ Manual API tests return expected responses
3. ✅ Frontend loads and displays correctly
4. ✅ User can register, login, and manage tasks
5. ✅ No security vulnerabilities detected
6. ✅ Performance meets requirements
7. ✅ Error handling works correctly
8. ✅ Logs show no critical errors

---

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Review this testing guide
3. Check the main README.md
4. Verify all prerequisites are met
5. Try restarting services: `./stop.sh && ./start.sh`

---

**Last Updated:** 2026-05-16  
**Version:** 1.0.0