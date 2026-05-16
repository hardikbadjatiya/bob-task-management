# 🚀 Deployment Guide - IBM Bob Hackathon Demo

## 📋 Deployment Options

Your application can be deployed on multiple platforms. Here are the recommended options:

---

## 🎯 Option 1: Docker-Based Deployment (Recommended)

### Quick Deploy with Docker Compose

The application is already containerized and ready to deploy anywhere that supports Docker.

#### Local Deployment
```bash
# Clone the repository
git clone https://github.com/[your-username]/ibm-bob-hackathon
cd ibm-bob-hackathon

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

#### Cloud Deployment Options

**AWS ECS/Fargate**
- Upload docker-compose.yml
- Configure environment variables
- Deploy containers

**Google Cloud Run**
- Deploy backend and frontend separately
- Configure Cloud SQL for PostgreSQL
- Set up Redis instance

**Azure Container Instances**
- Deploy multi-container group
- Configure Azure Database for PostgreSQL
- Set up Azure Cache for Redis

**DigitalOcean App Platform**
- Connect GitHub repository
- Auto-deploy from docker-compose.yml
- Built-in database and Redis

---

## 🌐 Option 2: Platform-as-a-Service (PaaS)

### Heroku Deployment

#### Backend (FastAPI)
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create ibm-bob-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Deploy
git push heroku main

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=postgresql://...
```

#### Frontend (React)
```bash
# Create frontend app
heroku create ibm-bob-frontend

# Set buildpack
heroku buildpacks:set heroku/nodejs

# Deploy
git subtree push --prefix frontend heroku main
```

**Demo URL**: `https://ibm-bob-backend.herokuapp.com`

---

## 🔷 Option 3: Vercel (Frontend) + Railway (Backend)

### Frontend on Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod

# Configure environment variables in Vercel dashboard
VITE_API_URL=https://your-backend-url.railway.app
```

**Demo URL**: `https://ibm-bob-hackathon.vercel.app`

### Backend on Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add PostgreSQL and Redis services
5. Configure environment variables
6. Deploy

**Backend URL**: `https://ibm-bob-backend.railway.app`

---

## 🎨 Option 4: Streamlit Cloud (Alternative Demo)

If you want to create a Streamlit demo interface:

### Create Streamlit App

```python
# streamlit_app.py
import streamlit as st
import requests

st.title("🤖 IBM Bob - Task Management Demo")

# API Configuration
API_URL = "https://your-backend-url.com/api/v1"

# Authentication
st.sidebar.header("Login")
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    response = requests.post(f"{API_URL}/auth/login", 
                           json={"email": email, "password": password})
    if response.status_code == 200:
        st.session_state.token = response.json()["access_token"]
        st.success("Logged in successfully!")

# Task Management
if "token" in st.session_state:
    st.header("Tasks")
    
    # Fetch tasks
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    tasks = requests.get(f"{API_URL}/tasks", headers=headers).json()
    
    # Display tasks
    for task in tasks:
        with st.expander(task["title"]):
            st.write(f"Status: {task['status']}")
            st.write(f"Priority: {task['priority']}")
            st.write(f"Description: {task['description']}")
    
    # Create new task
    st.subheader("Create New Task")
    title = st.text_input("Task Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    
    if st.button("Create Task"):
        response = requests.post(f"{API_URL}/tasks",
                               headers=headers,
                               json={"title": title, 
                                    "description": description,
                                    "priority": priority})
        if response.status_code == 201:
            st.success("Task created!")
            st.rerun()
```

### Deploy to Streamlit Cloud

1. Push `streamlit_app.py` to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Select `streamlit_app.py`
5. Add secrets in Streamlit dashboard:
   ```toml
   API_URL = "https://your-backend-url.com/api/v1"
   ```
6. Deploy

**Demo URL**: `https://ibm-bob-demo.streamlit.app`

---

## 🌟 Option 5: Render (Full-Stack)

### Deploy on Render

1. Go to [Render.com](https://render.com)
2. Create new Web Service for backend
3. Create new Static Site for frontend
4. Add PostgreSQL database
5. Add Redis instance
6. Configure environment variables
7. Deploy

**Frontend URL**: `https://ibm-bob-frontend.onrender.com`
**Backend URL**: `https://ibm-bob-backend.onrender.com`

---

## 📝 Deployment Checklist

### Pre-Deployment
- [ ] Update environment variables
- [ ] Configure CORS settings
- [ ] Set up database migrations
- [ ] Configure Redis connection
- [ ] Update API URLs in frontend
- [ ] Test locally with Docker
- [ ] Prepare deployment scripts

### Post-Deployment
- [ ] Verify all services are running
- [ ] Test authentication flow
- [ ] Test CRUD operations
- [ ] Check API documentation
- [ ] Monitor logs for errors
- [ ] Set up health checks
- [ ] Configure SSL/HTTPS
- [ ] Test from different devices

---

## 🔧 Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://host:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://your-frontend-url.com

# Environment
ENVIRONMENT=production
```

### Frontend (.env)
```bash
# API Configuration
VITE_API_URL=https://your-backend-url.com/api/v1

# Environment
VITE_ENVIRONMENT=production
```

---

## 🎯 Recommended Setup for Hackathon

### Best Option: Vercel + Railway + Streamlit

1. **Backend on Railway**
   - Automatic deployments from GitHub
   - Built-in PostgreSQL and Redis
   - Free tier available
   - URL: `https://ibm-bob-backend.railway.app`

2. **Frontend on Vercel**
   - Fast global CDN
   - Automatic deployments
   - Free tier available
   - URL: `https://ibm-bob-hackathon.vercel.app`

3. **Demo Interface on Streamlit** (Optional)
   - Interactive demo for judges
   - Easy to use interface
   - Free hosting
   - URL: `https://ibm-bob-demo.streamlit.app`

### Setup Time: ~30 minutes

---

## 📊 Monitoring & Logs

### Railway
```bash
# View logs
railway logs

# Check status
railway status
```

### Vercel
```bash
# View logs
vercel logs

# Check deployment
vercel inspect
```

### Heroku
```bash
# View logs
heroku logs --tail

# Check status
heroku ps
```

---

## 🔒 Security Considerations

### Production Checklist
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS only
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up monitoring
- [ ] Configure backup strategy
- [ ] Use secure database connections

---

## 🚨 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check DATABASE_URL format
postgresql://username:password@host:port/database

# Verify database is accessible
psql $DATABASE_URL
```

**CORS Errors**
```python
# Update backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Frontend Can't Connect to Backend**
```bash
# Check VITE_API_URL in frontend/.env
VITE_API_URL=https://your-backend-url.com/api/v1

# Rebuild frontend
npm run build
```

---

## 📱 Demo URLs Template

Update your [`HACKATHON_SUBMISSION.md`](./HACKATHON_SUBMISSION.md) with:

```markdown
## 🌐 Live Demo

### Application URLs
- **Frontend**: https://ibm-bob-hackathon.vercel.app
- **Backend API**: https://ibm-bob-backend.railway.app
- **API Documentation**: https://ibm-bob-backend.railway.app/api/docs
- **Interactive Demo**: https://ibm-bob-demo.streamlit.app

### Test Credentials
- Email: demo@example.com
- Password: Demo123!

### GitHub Repository
https://github.com/[your-username]/ibm-bob-hackathon
```

---

## 🎬 Quick Deploy Commands

### Deploy Everything in 5 Minutes

```bash
# 1. Deploy Backend to Railway
railway login
railway init
railway up

# 2. Deploy Frontend to Vercel
cd frontend
vercel --prod

# 3. (Optional) Deploy Streamlit Demo
# Push to GitHub, then deploy via Streamlit Cloud UI

# 4. Update URLs in submission
echo "Frontend: $(vercel inspect --prod | grep url)"
echo "Backend: $(railway status | grep url)"
```

---

## 💡 Pro Tips

1. **Use Free Tiers**: Railway, Vercel, and Streamlit all have generous free tiers
2. **Automate Deployments**: Connect GitHub for automatic deployments
3. **Monitor Performance**: Use built-in monitoring tools
4. **Prepare Demo Data**: Seed database with sample tasks
5. **Test Before Submission**: Verify all features work in production
6. **Have Backup**: Keep local Docker setup as backup
7. **Document URLs**: Update all documentation with live URLs

---

## 📞 Support

If you encounter issues:
1. Check platform-specific documentation
2. Review logs for error messages
3. Verify environment variables
4. Test locally first
5. Check CORS and security settings

---

**Ready to deploy? Choose your platform and follow the guide above!** 🚀