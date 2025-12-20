# 🚀 GitHub Auto-Deploy Guide

## 3 Ways to Deploy with GitHub

---

## ✨ **Option 1: GitHub → Render.com (EASIEST, FREE)**

### **This is the simplest! No servers needed!**

### Steps:

1. **Push your code to GitHub:**

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

2. **Deploy to Render.com:**
   - Go to **[render.com](https://render.com)** and sign up (free)
   - Click **"New +"** → **"Web Service"**
   - Connect your **GitHub account**
   - Select your repository
   - Render auto-detects settings from `render.yaml`
   - Click **"Create Web Service"**

3. **Done!** 🎉
   - Render gives you a URL like: `https://your-app.onrender.com`
   - **Every push to GitHub = Automatic deployment**
   - No server management needed!

### Pros:
- ✅ **100% Free** (with auto-sleep)
- ✅ **Zero configuration**
- ✅ **Auto-deploy on git push**
- ✅ **Free SSL certificate**
- ✅ **No server management**

### Cons:
- ⚠️ Free tier sleeps after 15 min inactivity
- ⚠️ Takes ~30 seconds to wake up

---

## 🔥 **Option 2: GitHub → Railway.app (SIMPLE, $5/month)**

### **Best balance of simplicity and performance**

### Steps:

1. **Push code to GitHub** (same as above)

2. **Deploy to Railway:**
   - Go to **[railway.app](https://railway.app)**
   - Sign in with GitHub
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your repository
   - Railway auto-detects and deploys

3. **Done!** 🎉
   - Always running (no sleep)
   - Auto-deploys on push
   - Custom domain support

### Pricing:
- Free $5 credit/month
- After that: ~$5-10/month depending on usage

---

## 🛠️ **Option 3: GitHub → Your VPS (Full Control, $5-10/month)**

### **For maximum control and customization**

### Initial Setup (One-time):

1. **Get a VPS:**
   - DigitalOcean ($6/month)
   - Linode ($5/month)
   - AWS EC2 ($8/month)
   - Any Linux server

2. **Deploy initially:**

```bash
# On your VPS:
ssh your-server

# Clone your repo
cd /opt
sudo git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git jobsearch
cd jobsearch

# Run deployment script
bash deploy/quick_deploy.sh
```

3. **Set up GitHub Actions for auto-deploy:**

#### a. Generate SSH key on your VPS:

```bash
ssh-keygen -t ed25519 -C "github-actions"
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/id_ed25519  # Copy this private key
```

#### b. Add secrets to GitHub:

- Go to your GitHub repo
- Click **Settings** → **Secrets and variables** → **Actions**
- Click **"New repository secret"**

Add these 3 secrets:

| Secret Name | Value |
|-------------|-------|
| `VPS_HOST` | Your server IP (e.g., `123.45.67.89`) |
| `VPS_USERNAME` | Your username (e.g., `ubuntu`) |
| `VPS_SSH_KEY` | Your private SSH key (from above) |

#### c. Push to GitHub:

```bash
git add .
git commit -m "Add auto-deploy"
git push origin main
```

4. **Done!** 🎉
   - Every push to `main` = Auto-deploy
   - GitHub Actions runs the deploy script
   - App restarts automatically

---

## 📊 **Comparison Table**

| Feature | Render.com | Railway.app | Your VPS |
|---------|------------|-------------|----------|
| **Cost** | Free | $5/mo | $5-10/mo |
| **Setup Time** | 5 min | 5 min | 20 min |
| **Auto-Deploy** | ✅ Yes | ✅ Yes | ✅ Yes (with Actions) |
| **Always On** | ❌ Sleeps | ✅ Yes | ✅ Yes |
| **Custom Domain** | ✅ Yes | ✅ Yes | ✅ Yes |
| **SSL/HTTPS** | ✅ Auto | ✅ Auto | Manual |
| **Full Control** | ❌ No | ⚠️ Limited | ✅ Yes |

---

## 🎯 **Which Should You Choose?**

### Choose **Render.com** if:
- You want FREE hosting
- You don't mind 30s wake-up time
- You want zero configuration
- **Recommended for: Personal projects, demos**

### Choose **Railway.app** if:
- You want always-on service
- You want simple management
- You can spend $5/month
- **Recommended for: Small production apps**

### Choose **VPS** if:
- You want full control
- You want to learn server management
- You need custom configurations
- **Recommended for: Serious production apps**

---

## 🚀 **Quick Start Commands**

### For Render.com or Railway.app:

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# 2. Go to render.com or railway.app
# 3. Connect GitHub repo
# 4. Done! ✅
```

### For VPS with GitHub Actions:

```bash
# 1. Initial deploy on VPS
ssh your-server
cd /opt
sudo git clone YOUR_REPO_URL jobsearch
cd jobsearch
bash deploy/quick_deploy.sh

# 2. Set up GitHub secrets (see above)

# 3. Push code
git add .
git commit -m "Deploy"
git push origin main

# 4. GitHub Actions auto-deploys! ✅
```

---

## 🔍 **Monitor Your Deployments**

### Render.com:
- Dashboard shows deployment logs
- Click on your service → "Logs"

### Railway.app:
- Dashboard shows build progress
- Click on your service → "Deployments"

### VPS with GitHub Actions:
- Go to GitHub repo → "Actions" tab
- See deployment status and logs

---

## 🎉 **My Recommendation for You**

Start with **Render.com**:
1. Takes 5 minutes
2. 100% free
3. Auto-deploys from GitHub
4. No credit card needed
5. You can upgrade later if needed

**Steps:**
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to render.com
# 3. Connect repo
# 4. Click deploy
# 5. Get your URL in 2 minutes!
```

---

## 🆘 **Need Help?**

Let me know which option you choose, and I'll give you the exact step-by-step commands!

**Want me to help you deploy right now?** Tell me:
1. Do you have a GitHub account? (Yes/No)
2. Which option do you prefer? (Render/Railway/VPS)
