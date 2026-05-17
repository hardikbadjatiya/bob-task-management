# 🚀 Step-by-Step Vercel Deployment Guide

## Overview

This guide will walk you through deploying your IBM Bob Hackathon project:
- **Frontend** → Vercel (React + TypeScript)
- **Backend** → Railway (FastAPI + PostgreSQL + Redis)

**Estimated Time**: 20-30 minutes

---

## 📋 Prerequisites

Before starting, ensure you have:
- [ ] GitHub account
- [ ] Vercel account (sign up at [vercel.com](https://vercel.com))
- [ ] Railway account (sign up at [railway.app](https://railway.app))
- [ ] Your code pushed to GitHub repository
- [ ] Basic understanding of environment variables

---

## Part 1: Deploy Backend on Railway (15 minutes)

### Step 1: Create Railway Account & Project

1. **Go to [Railway.app](https://railway.app)**
2. Click **"Start a New Project"**
3. Choose **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `ibm-bob-hackathon` repository

### Step 2: Add PostgreSQL Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will automatically create a PostgreSQL instance
4. Note: The `DATABASE_URL` will be automatically available as an environment variable

### Step 3: Add Redis Cache

1. Click **"+ New"** again
2. Select **"Database"** → **"Redis"**
3. Railway will create a Redis instance
4. Note: The `REDIS_URL` will be automatically available

### Step 4: Configure Backend Service

1. Click on your backend service (the one connected to GitHub)
2. Go to **"Settings"** tab
3. Under **"Root Directory"**, set it to: `backend`
4. Under **"Start Command"**, set it to:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Step 5: Set Environment Variables

1. Go to **"Variables"** tab in your backend service
2. Add the following environment variables:

```bash
# Security
SECRET_KEY=your-super-secret-key-min-32-characters-long-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Update after deploying frontend
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app

# Environment
ENVIRONMENT=production

# Database (automatically set by Railway, but verify)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (automatically set by Railway, but verify)
REDIS_URL=${{Redis.REDIS_URL}}
```

**Important Notes:**
- Railway automatically injects `DATABASE_URL` and `REDIS_URL` from your database services
- Generate a strong `SECRET_KEY` using: `openssl rand -hex 32`
- You'll update `ALLOWED_ORIGINS` after deploying the frontend

### Step 6: Deploy Backend

1. Click **"Deploy"** or push changes to GitHub
2. Railway will automatically build and deploy
3. Wait for deployment to complete (2-5 minutes)
4. Once deployed, click on your service to get the URL
5. **Copy your backend URL**: `https://your-backend-name.up.railway.app`

### Step 7: Test Backend

1. Visit: `https://your-backend-name.up.railway.app/api/docs`
2. You should see the Swagger API documentation
3. Test the health endpoint: `https://your-backend-name.up.railway.app/api/v1/health`

---

## Part 2: Deploy Frontend on Vercel (10 minutes)

### Step 1: Prepare Frontend Configuration

Before deploying, ensure your frontend is configured correctly:

1. **Update `frontend/.env.example`** (if not already done):
```bash
VITE_API_URL=https://your-backend-name.up.railway.app/api/v1
VITE_ENVIRONMENT=production
```

2. **Verify `frontend/vite.config.ts`** includes:
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  },
  preview: {
    port: 3000,
    host: true
  }
})
```

### Step 2: Create Vercel Account & Import Project

1. **Go to [Vercel.com](https://vercel.com)**
2. Click **"Add New..."** → **"Project"**
3. Click **"Import Git Repository"**
4. Authorize Vercel to access your GitHub
5. Select your `ibm-bob-hackathon` repository
6. Click **"Import"**

### Step 3: Configure Project Settings

Vercel will detect it's a monorepo. Configure as follows:

1. **Framework Preset**: Select **"Vite"**
2. **Root Directory**: Click **"Edit"** and set to `frontend`
3. **Build Command**: 
   ```bash
   npm run build
   ```
4. **Output Directory**: 
   ```bash
   dist
   ```
5. **Install Command**: 
   ```bash
   npm install
   ```

### Step 4: Set Environment Variables

1. Expand **"Environment Variables"** section
2. Add the following variables:

```bash
VITE_API_URL=https://your-backend-name.up.railway.app/api/v1
VITE_ENVIRONMENT=production
```

**Replace** `your-backend-name.up.railway.app` with your actual Railway backend URL from Part 1, Step 6.

### Step 5: Deploy Frontend

1. Click **"Deploy"**
2. Vercel will build and deploy your frontend (2-3 minutes)
3. Wait for the deployment to complete
4. Once done, you'll see: **"Congratulations! Your project has been deployed."**
5. **Copy your frontend URL**: `https://your-project-name.vercel.app`

### Step 6: Update Backend CORS Settings

Now that you have your frontend URL, update the backend:

1. Go back to **Railway dashboard**
2. Open your **backend service**
3. Go to **"Variables"** tab
4. Update `ALLOWED_ORIGINS`:
   ```bash
   ALLOWED_ORIGINS=https://your-project-name.vercel.app,http://localhost:3000
   ```
5. Click **"Save"**
6. Railway will automatically redeploy with new settings

### Step 7: Test Your Application

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. You should see your application's login page
3. Try to register a new user
4. Try to login
5. Create some tasks

---

## Part 3: Verification & Testing (5 minutes)

### Checklist

- [ ] Backend is accessible at Railway URL
- [ ] API docs work: `https://your-backend.railway.app/api/docs`
- [ ] Frontend loads at Vercel URL
- [ ] Can register a new user
- [ ] Can login successfully
- [ ] Can create tasks
- [ ] Can view tasks
- [ ] Can update tasks
- [ ] Can delete tasks
- [ ] No CORS errors in browser console

### Common Issues & Solutions

#### Issue 1: CORS Error
**Symptom**: Browser console shows CORS policy error

**Solution**:
1. Check `ALLOWED_ORIGINS` in Railway backend variables
2. Ensure it includes your Vercel URL (with https://)
3. No trailing slash in the URL
4. Redeploy backend after changes

#### Issue 2: API Connection Failed
**Symptom**: Frontend can't connect to backend

**Solution**:
1. Verify `VITE_API_URL` in Vercel environment variables
2. Ensure it includes `/api/v1` at the end
3. Check backend is running on Railway
4. Redeploy frontend after changes

#### Issue 3: Database Connection Error
**Symptom**: Backend shows database errors

**Solution**:
1. Check PostgreSQL service is running on Railway
2. Verify `DATABASE_URL` is set correctly
3. Check Railway logs for specific errors

#### Issue 4: 404 on Frontend Routes
**Symptom**: Refreshing page shows 404

**Solution**:
1. Add `vercel.json` in frontend directory:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```
2. Commit and push to trigger redeployment

---

## Part 4: Custom Domain (Optional)

### Add Custom Domain to Vercel

1. Go to your project in Vercel
2. Click **"Settings"** → **"Domains"**
3. Enter your domain name
4. Follow Vercel's instructions to configure DNS
5. Wait for DNS propagation (can take up to 48 hours)

### Add Custom Domain to Railway

1. Go to your backend service in Railway
2. Click **"Settings"** → **"Domains"**
3. Click **"Generate Domain"** or add custom domain
4. Update `ALLOWED_ORIGINS` in backend to include new domain

---

## Part 5: Continuous Deployment

### Automatic Deployments

Both Vercel and Railway support automatic deployments:

**Vercel (Frontend)**:
- Automatically deploys on every push to `main` branch
- Preview deployments for pull requests
- Instant rollbacks available

**Railway (Backend)**:
- Automatically deploys on every push to `main` branch
- Can configure deployment triggers
- View deployment logs in real-time

### Manual Deployment

**Vercel**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from command line
cd frontend
vercel --prod
```

**Railway**:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway up
```

---

## Part 6: Monitoring & Logs

### View Logs

**Railway Backend Logs**:
1. Go to Railway dashboard
2. Click on your backend service
3. Click **"Deployments"** tab
4. Click on latest deployment
5. View real-time logs

**Vercel Frontend Logs**:
1. Go to Vercel dashboard
2. Click on your project
3. Click **"Deployments"** tab
4. Click on latest deployment
5. View build and runtime logs

### Monitor Performance

**Railway**:
- View CPU and Memory usage in dashboard
- Set up alerts for service downtime
- Monitor database connections

**Vercel**:
- View analytics in dashboard
- Monitor Core Web Vitals
- Track page load times

---

## Part 7: Update Submission Materials

### Update URLs in Documentation

1. **Update `HACKATHON_SUBMISSION.md`**:
```markdown
### Application URLs
- **Frontend**: https://your-project-name.vercel.app
- **Backend API**: https://your-backend-name.up.railway.app
- **API Documentation**: https://your-backend-name.up.railway.app/api/docs
```

2. **Update `README.md`**:
```markdown
## 🌐 Live Demo

- **Application**: https://your-project-name.vercel.app
- **API Docs**: https://your-backend-name.up.railway.app/api/docs
```

3. **Commit and push changes**:
```bash
git add .
git commit -m "Update deployment URLs"
git push origin main
```

---

## 📊 Deployment Summary

### Your Deployed Application

| Service | Platform | URL | Status |
|---------|----------|-----|--------|
| Frontend | Vercel | `https://your-project.vercel.app` | ✅ |
| Backend | Railway | `https://your-backend.railway.app` | ✅ |
| Database | Railway | PostgreSQL (internal) | ✅ |
| Cache | Railway | Redis (internal) | ✅ |
| API Docs | Railway | `https://your-backend.railway.app/api/docs` | ✅ |

### Cost Breakdown

**Vercel**:
- Free tier: Unlimited deployments
- Bandwidth: 100GB/month
- Build time: 6000 minutes/month

**Railway**:
- Free tier: $5 credit/month
- Includes: PostgreSQL, Redis, Backend hosting
- Typically sufficient for hackathon demos

**Total Cost**: $0 (within free tiers)

---

## 🎯 Quick Reference Commands

### Vercel CLI
```bash
# Install
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls
```

### Railway CLI
```bash
# Install
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up

# View logs
railway logs

# Open dashboard
railway open
```

---

## 🔧 Troubleshooting Guide

### Backend Issues

**Problem**: Backend won't start
```bash
# Check Railway logs
railway logs

# Common fixes:
# 1. Verify requirements.txt is correct
# 2. Check DATABASE_URL is set
# 3. Ensure PORT is used: --port $PORT
```

**Problem**: Database connection fails
```bash
# Verify DATABASE_URL format
# Should be: postgresql://user:pass@host:port/db

# Check PostgreSQL service is running
# In Railway dashboard → PostgreSQL service
```

### Frontend Issues

**Problem**: Build fails on Vercel
```bash
# Check build logs in Vercel dashboard
# Common fixes:
# 1. Verify package.json scripts
# 2. Check TypeScript errors
# 3. Ensure all dependencies are listed
```

**Problem**: Environment variables not working
```bash
# Vercel requires VITE_ prefix for Vite apps
# Correct: VITE_API_URL
# Wrong: API_URL

# Redeploy after changing env vars
vercel --prod
```

---

## ✅ Final Checklist

Before submitting your hackathon project:

- [ ] Backend deployed and accessible on Railway
- [ ] Frontend deployed and accessible on Vercel
- [ ] API documentation accessible
- [ ] Can register new users
- [ ] Can login successfully
- [ ] Can perform CRUD operations on tasks
- [ ] No console errors
- [ ] CORS configured correctly
- [ ] Environment variables set properly
- [ ] URLs updated in all documentation
- [ ] Tested on multiple devices/browsers
- [ ] Screenshots taken for submission
- [ ] Demo video recorded (if required)

---

## 🎉 Congratulations!

Your application is now live and ready for the hackathon submission!

**Next Steps**:
1. Test all features thoroughly
2. Take screenshots for your presentation
3. Update submission materials with live URLs
4. Prepare your demo video
5. Submit to the hackathon!

**Need Help?**
- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Project Issues: GitHub Issues tab

---

**Deployment Complete! 🚀**

Your IBM Bob Hackathon project is now live and accessible to judges and users worldwide!