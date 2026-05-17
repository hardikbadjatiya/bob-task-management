# 🔧 Deployment Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Issue 1: Vercel Environment Variable Error ✅ FIXED

**Error Message**:
```
Environment Variable "VITE_API_URL" references Secret "vite_api_url", which does not exist.
```

**Root Cause**: The `vercel.json` file was trying to reference a Vercel Secret that doesn't exist.

**Solution**: ✅ **FIXED** - Removed the secret reference from `vercel.json`. Now set environment variables directly in Vercel dashboard.

**Steps to Deploy**:
1. Remove the `env` section from `vercel.json` (already done)
2. Set environment variables in Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend-url.railway.app/api/v1`
3. Redeploy

---

### Issue 2: Login Failed - API Path Mismatch ✅ FIXED

**Error Message**:
```
Login failed
```

**Root Cause**: Frontend services were using incorrect API paths with double `/api/v1` prefix.

**Solution**: ✅ **FIXED** - Updated all service files to use correct paths:
- ❌ Before: `/api/v1/auth/login` (incorrect - double prefix)
- ✅ After: `/auth/login` (correct - base URL already includes `/api/v1`)

**Files Fixed**:
- `frontend/src/services/authService.ts`
- `frontend/src/services/taskService.ts`
- `frontend/src/services/api.ts`

---

### Issue 3: CORS Errors

**Symptoms**:
- Browser console shows CORS policy errors
- API requests fail with 403 or blocked by CORS

**Solution**:
1. Update backend `CORS_ORIGINS` environment variable:
   ```bash
   CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
   ```
2. Ensure no trailing slashes in URLs
3. Redeploy backend after changes

---

### Issue 4: Database Connection Failed

**Symptoms**:
- Backend shows database connection errors
- 500 errors on API requests

**Solution**:
1. Verify `DATABASE_URL` is set correctly in Railway
2. Check PostgreSQL service is running
3. Verify connection string format:
   ```
   postgresql://user:password@host:port/database
   ```
4. Check Railway logs for specific errors

---

### Issue 5: 404 on Frontend Routes

**Symptoms**:
- Refreshing page shows 404
- Direct URL access fails

**Solution**: ✅ Already configured in `vercel.json`:
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

---

## 🔍 Debugging Checklist

### Frontend Issues

- [ ] Check browser console for errors
- [ ] Verify `VITE_API_URL` is set correctly
- [ ] Check network tab for failed requests
- [ ] Verify API base URL doesn't have double prefixes
- [ ] Check if backend is accessible
- [ ] Clear browser cache and localStorage

### Backend Issues

- [ ] Check Railway logs for errors
- [ ] Verify all environment variables are set
- [ ] Check database connection
- [ ] Verify Redis connection
- [ ] Test API endpoints directly (Postman/curl)
- [ ] Check CORS configuration

### Authentication Issues

- [ ] Verify demo user exists in database
- [ ] Check JWT secret is set
- [ ] Verify token expiration settings
- [ ] Check password hashing is working
- [ ] Test login endpoint directly

---

## 🧪 Testing Endpoints

### Test Backend Health
```bash
curl https://your-backend.railway.app/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Test Login
```bash
curl -X POST https://your-backend.railway.app/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=Demo123!"
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Test Tasks Endpoint
```bash
curl https://your-backend.railway.app/api/v1/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📊 Environment Variables Reference

### Frontend (Vercel)

| Variable | Example | Required |
|----------|---------|----------|
| `VITE_API_URL` | `https://backend.railway.app/api/v1` | ✅ Yes |
| `VITE_ENVIRONMENT` | `production` | ❌ No |

### Backend (Railway)

| Variable | Example | Required |
|----------|---------|----------|
| `DATABASE_URL` | `postgresql://...` | ✅ Yes |
| `REDIS_URL` | `redis://...` | ✅ Yes |
| `SECRET_KEY` | `your-secret-key` | ✅ Yes |
| `ALGORITHM` | `HS256` | ✅ Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | ✅ Yes |
| `CORS_ORIGINS` | `https://app.vercel.app` | ✅ Yes |
| `ENVIRONMENT` | `production` | ❌ No |

---

## 🚀 Quick Deployment Commands

### Redeploy Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Redeploy Backend (Railway)
```bash
# Push to main branch triggers auto-deploy
git push origin main

# Or use Railway CLI
railway up
```

### View Logs
```bash
# Vercel
vercel logs

# Railway
railway logs
```

---

## 🔐 Security Checklist

- [ ] No secrets in code
- [ ] Environment variables set properly
- [ ] CORS configured correctly
- [ ] HTTPS enforced
- [ ] Strong JWT secret (32+ characters)
- [ ] Password hashing enabled
- [ ] Rate limiting configured
- [ ] Security headers enabled

---

## 📞 Getting Help

### Check Logs First
1. **Vercel**: Project → Deployments → Latest → View Function Logs
2. **Railway**: Service → Deployments → Latest → View Logs

### Common Log Locations
- Frontend build errors: Vercel deployment logs
- Runtime errors: Browser console
- Backend errors: Railway service logs
- Database errors: Railway PostgreSQL logs

### Debug Mode
Enable debug logging:
```bash
# Backend
DEBUG=true

# Frontend
VITE_ENABLE_DEBUG=true
```

---

## ✅ Deployment Success Checklist

- [ ] Frontend deploys successfully on Vercel
- [ ] Backend deploys successfully on Railway
- [ ] Database is accessible
- [ ] Redis is accessible
- [ ] Environment variables are set
- [ ] CORS is configured
- [ ] Login works with demo credentials
- [ ] Tasks can be fetched
- [ ] No console errors
- [ ] API documentation accessible
- [ ] Health check passes

---

## 🎯 Quick Fixes

### Reset Everything
```bash
# Clear browser storage
localStorage.clear()
sessionStorage.clear()

# Redeploy frontend
cd frontend && vercel --prod

# Restart backend
# In Railway: Service → Settings → Restart
```

### Test Locally First
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Start frontend
cd frontend
npm run dev

# Test login at http://localhost:3000
```

---

## 📝 Notes

- Always test locally before deploying
- Check logs immediately after deployment
- Verify environment variables are set
- Test with demo credentials first
- Keep backup of working configuration

---

**Last Updated**: 2026-05-17  
**Status**: All critical issues resolved ✅