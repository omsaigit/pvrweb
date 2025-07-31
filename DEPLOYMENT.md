# PVR Trading Dashboard - Deployment Guide

## Free Hosting Options

### 1. Render (Recommended - Free Tier)
**Best option for Flask apps with real-time features**

#### Steps:
1. **Sign up** at [render.com](https://render.com)
2. **Connect your GitHub repository**:
   - Push your code to GitHub
   - In Render dashboard, click "New +" → "Web Service"
   - Connect your GitHub repo
3. **Configure the service**:
   - **Name**: `pvr-trading-dashboard`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
   - **Plan**: Free
4. **Deploy**: Click "Create Web Service"

#### Features:
- ✅ Free tier available
- ✅ Automatic deployments from Git
- ✅ Custom domains
- ✅ SSL certificates
- ✅ 750 hours/month free
- ✅ Sleeps after 15 minutes of inactivity

---

### 2. Railway (Alternative)
**Good for real-time apps**

#### Steps:
1. **Sign up** at [railway.app](https://railway.app)
2. **Deploy from GitHub**:
   - Connect your GitHub repo
   - Railway will auto-detect Python
   - Deploy automatically
3. **Configure**:
   - Add environment variables if needed
   - Set custom domain (optional)

#### Features:
- ✅ Free tier available
- ✅ Real-time deployments
- ✅ Custom domains
- ✅ 500 hours/month free

---

### 3. Heroku (Alternative)
**Classic option but limited free tier**

#### Steps:
1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: `git push heroku main`

#### Features:
- ⚠️ No free tier (paid plans only)
- ✅ Very reliable
- ✅ Great documentation

---

### 4. PythonAnywhere (Alternative)
**Good for Python-specific hosting**

#### Steps:
1. **Sign up** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload files** via web interface
3. **Configure WSGI file**
4. **Set up virtual environment**

#### Features:
- ✅ Free tier available
- ✅ Python-focused
- ⚠️ Limited bandwidth on free tier

---

## Important Notes

### Environment Variables
If your app uses sensitive data (API keys, tokens), set them as environment variables in your hosting platform:

```bash
# Example environment variables to set
KITE_API_KEY=your_api_key
KITE_SECRET=your_secret
```

### File Structure
Make sure your project has these files:
```
pvr/
├── web_app.py          # Main Flask app
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html
├── config.json         # Configuration
├── render.yaml         # Render config
├── Procfile           # Heroku config
├── gunicorn.conf.py   # Gunicorn config
└── runtime.txt        # Python version
```

### Database Considerations
- Free tiers usually don't include persistent databases
- Consider using external database services if needed
- For demo purposes, file-based storage works fine

### Real-time Features
- WebSocket connections may not work on free tiers
- Use polling for real-time updates (your current approach)
- Consider upgrading to paid plans for better real-time support

## Quick Deploy Commands

### Render (via CLI)
```bash
# Install Render CLI
curl -sL https://render.com/download-cli/linux | bash

# Deploy
render deploy
```

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway up
```

### Heroku
```bash
# Deploy
git push heroku main

# Open app
heroku open
```

## Troubleshooting

### Common Issues:
1. **Port binding**: Make sure your app binds to `0.0.0.0` and uses `$PORT` environment variable
2. **Dependencies**: Ensure all dependencies are in `requirements.txt`
3. **Static files**: Serve static files through Flask or use a CDN
4. **Environment variables**: Set sensitive data as environment variables

### Debug Commands:
```bash
# Check logs
render logs

# SSH into container (if available)
render shell

# Check app status
render ps
```

## Recommended: Render Deployment

**Why Render is recommended:**
- ✅ Generous free tier
- ✅ Easy deployment from GitHub
- ✅ Good for Flask apps
- ✅ Automatic SSL
- ✅ Custom domains
- ✅ Good documentation

**Deployment time**: ~5-10 minutes
**Cost**: Free (with limitations)
**Uptime**: 99.9% (sleeps after inactivity)

---

## Next Steps

1. **Choose a hosting platform** (recommend Render)
2. **Push code to GitHub**
3. **Follow platform-specific deployment steps**
4. **Configure environment variables**
5. **Test your deployed app**
6. **Set up custom domain** (optional)

Your PVR Trading Dashboard should be live and accessible from anywhere! 🚀 