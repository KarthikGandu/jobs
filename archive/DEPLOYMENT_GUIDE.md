# 🚀 Deployment Guide - Host Your Job Search Website

## 🎯 Best Option: Render.com (FREE!)

Render.com is the best free hosting for Flask apps. Here's how to deploy:

---

## 📋 Prerequisites

1. **GitHub Account** (create at github.com if you don't have one)
2. **Render Account** (create at render.com - it's free!)
3. **Your code** (already ready!)

---

## 🚀 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
# 1. Initialize git repository (if not already done)
cd /path/to/your/project
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit - Karthik's Job Search Site"

# 4. Create repository on GitHub.com
# Go to github.com → Click "+" → "New repository"
# Name it: karthik-job-search
# Make it Public or Private (your choice)
# DON'T initialize with README (we already have one)

# 5. Link to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/karthik-job-search.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render.com

1. **Go to** https://render.com and sign up (free)

2. **Click** "New +" → "Web Service"

3. **Connect GitHub**: 
   - Click "Connect GitHub"
   - Authorize Render
   - Select your repository: `karthik-job-search`

4. **Configure**:
   - **Name**: `karthik-job-search`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. **Plan**: Select "Free" (FREE TIER!)

6. **Click** "Create Web Service"

7. **Wait** 5-10 minutes for deployment

8. **Your site will be live at**: 
   ```
   https://karthik-job-search.onrender.com
   ```

---

## ⚙️ Files Already Created for Render

✅ `render.yaml` - Render configuration
✅ `requirements.txt` - Updated with gunicorn
✅ `.gitignore` - Ignores unnecessary files
✅ All your Python files ready

---

## 🎯 After Deployment

### Your website will be live at:
```
https://karthik-job-search.onrender.com
```

### Features:
- ✅ Fully functional Flask backend
- ✅ All 24 company scrapers working
- ✅ Indeed + LinkedIn scraping
- ✅ ML filtering active
- ✅ CSV downloads working
- ✅ Beautiful UI live

### Limitations (Free Tier):
- ⚠️ Site "sleeps" after 15 minutes of inactivity
- ⚠️ First visit after sleep takes 30-60 seconds to wake up
- ⚠️ 750 hours/month free (more than enough!)
- ⚠️ Limited to 512MB RAM

---

## 🔄 Updating Your Website

Whenever you make changes:

```bash
# 1. Make your changes
# 2. Commit
git add .
git commit -m "Updated feature X"

# 3. Push to GitHub
git push origin main

# 4. Render auto-deploys (3-5 minutes)
# Your site automatically updates!
```

---

## 🆓 Alternative Free Options

### Option 2: Railway.app
- Similar to Render
- Free tier: 500 hours/month
- Same deployment process
- Website: railway.app

### Option 3: Fly.io
- More technical
- Free tier: 3 VMs
- Requires Docker knowledge
- Website: fly.io

### Option 4: PythonAnywhere
- Specifically for Python
- Free tier: 1 web app
- Limited to 100k requests/day
- Website: pythonanywhere.com

---

## 💰 Paid Options (If You Need Better Performance)

### Render (Paid)
- **$7/month**: No sleep, faster, 512MB RAM
- **$25/month**: 2GB RAM, priority support

### Heroku
- **$7/month**: Basic dyno, no sleep
- **$25/month**: Standard dyno, better performance

### DigitalOcean
- **$5/month**: VPS (requires setup)
- **$12/month**: App Platform (managed)

---

## 🔧 Troubleshooting

### Issue: "Application Error" on Render
**Solution**: Check Render logs:
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. Look for errors

Common fixes:
- Check `requirements.txt` has all dependencies
- Ensure `gunicorn app:app` command is correct
- Verify `app.py` exists

### Issue: Site is slow
**Solution**: 
- Normal on free tier after wake-up
- Consider paid tier for always-on
- First load: 30-60 seconds
- After that: Fast!

### Issue: Can't scrape companies
**Solution**:
- Some companies might block Render's IPs
- Works for most firms
- Indeed + LinkedIn should always work

---

## 📊 What Works on Render (Free Tier)

### ✅ Will Work:
- Flask backend ✓
- Indeed scraping ✓
- LinkedIn scraping ✓
- Most company scrapers ✓
- ML filtering ✓
- Keyword expansion ✓
- CSV downloads ✓
- Beautiful UI ✓

### ⚠️ May Have Issues:
- Some companies might block cloud IPs
- Slower than localhost
- Cold starts (30-60 sec)

### ❌ Won't Work:
- Nothing! Everything should work on Render

---

## 🎯 Recommended Workflow

### For Development:
```bash
# Test locally
python3 app.py
# Visit: http://localhost:5001
```

### For Production:
```bash
# Push to GitHub
git push origin main
# Render auto-deploys
# Visit: https://karthik-job-search.onrender.com
```

---

## 🔐 Environment Variables (If Needed)

If you need to add API keys or secrets:

1. In Render dashboard → Your service
2. Go to "Environment" tab
3. Add variables:
   ```
   KEY_NAME = value
   ```
4. Click "Save Changes"
5. Service auto-restarts

---

## 📝 Custom Domain (Optional)

### Free Subdomain:
```
https://karthik-job-search.onrender.com
```

### Custom Domain ($):
1. Buy domain (e.g., karthikjobs.com) - $10-15/year
2. In Render: Settings → Custom Domains
3. Add your domain
4. Update DNS records
5. Done!

---

## 🎉 Summary

**Best Free Option: Render.com**

**Steps:**
1. Push code to GitHub (5 minutes)
2. Deploy on Render (10 minutes)
3. Share your link! (instant)

**Total Time:** 15 minutes
**Cost:** $0 (FREE!)

**Your live website:**
```
https://karthik-job-search.onrender.com
```

---

## 🚀 Quick Commands

```bash
# Initialize and push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/karthik-job-search.git
git push -u origin main

# That's it! Then deploy on Render.com via their UI
```

---

**Ready to deploy?** Follow the steps above and your site will be live in 15 minutes! 🎉

---

**© 2025 Karthik. All rights reserved.**

*From localhost to worldwide - your job search site is going live!*
