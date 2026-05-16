# 🚀 Quick Start Guide

## Start the Application (3 Steps)

### 1. Start Docker Desktop
Ensure Docker Desktop is running on your machine.

### 2. Run the Startup Script
```bash
./start.sh
```

### 3. Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Test the Application

```bash
./test.sh
```

Expected: All 10 tests pass ✅

---

## Stop the Application

```bash
./stop.sh
```

---

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`start.sh`](start.sh:1) | Start with Docker | `./start.sh` |
| [`stop.sh`](stop.sh:1) | Stop Docker containers | `./stop.sh` |
| [`start-dev.sh`](start-dev.sh:1) | Start locally (no Docker) | `./start-dev.sh` |
| [`test.sh`](test.sh:1) | Run automated tests | `./test.sh` |
| [`validate.sh`](validate.sh:1) | Validate project structure | `./validate.sh` |

---

## Documentation

- 📖 **Full Documentation:** [`README.md`](README.md:1)
- 🧪 **Testing Guide:** [`TESTING_GUIDE.md`](TESTING_GUIDE.md:1)
- 📊 **Test Results:** [`TEST_RESULTS.md`](TEST_RESULTS.md:1)
- 🎯 **Hackathon Plan:** [`HACKATHON_PLAN.md`](HACKATHON_PLAN.md:1)
- 📈 **Project Status:** [`PROJECT_STATUS.md`](PROJECT_STATUS.md:1)

---

## Troubleshooting

### Docker not running?
Start Docker Desktop and try again.

### Port already in use?
```bash
# Check what's using the port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Or change ports in docker-compose.yml
```

### Need to reset everything?
```bash
docker-compose down -v  # Remove all data
./start.sh              # Start fresh
```

---

## Default Credentials

Create a new account at http://localhost:3000 or use the API:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

---

**Need Help?** Check [`TESTING_GUIDE.md`](TESTING_GUIDE.md:1) for detailed instructions.