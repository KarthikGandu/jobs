# 🚀 How to Run the Complete Platform Locally

## 📋 Prerequisites

- Python 3.8+ installed
- Git installed

---

## ⚡ Quick Start (5 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask + extensions (Login, SQLAlchemy, Bcrypt)
- Resume parsing (PyPDF2, python-docx)
- Job scraping libraries
- All other dependencies

---

### Step 2: Run the App

```bash
python run.py
```

Or use the Makefile:

```bash
make restart
```

---

### Step 3: Open in Browser

```
http://localhost:5000
```

---

### Step 4: Create an Account

1. Click **"Sign up"**
2. Fill in:
   - Full Name
   - Email
   - Username
   - Password (min 6 characters)
3. Click **"Create Account"**
4. You'll see a splash screen, then the dashboard!

---

### Step 5: Upload Resume (Optional)

1. Click **"📄 Upload Resume to Get Match Scores"**
2. Drag & drop or click to upload PDF/DOCX
3. Wait for parsing (~5 seconds)
4. Now search jobs and see match scores!

---

## 🎯 What Happens First Time

### Database Auto-Created:
- File: `job_search.db` (SQLite)
- Tables: `users`, `resumes`, `job_applications`
- Location: Root directory

### Folder Created:
- `uploads/resumes/` - Stores uploaded resumes

### You Can:
- ✅ Search jobs (works without resume)
- ✅ Upload resume (to get match scores)
- ✅ See match percentages (after resume upload)

---

## 🔧 Useful Commands

### Restart App (Kills old, starts new):
```bash
make restart
```

### Stop App:
```bash
make stop
```

### View Logs:
```bash
make logs
# or
tail -f job_search_app.log
```

### Check App Status:
```bash
make status
```

---

## 🧪 Test It Works

### 1. Test Authentication:
```bash
# Open browser
http://localhost:5000

# Should redirect to login page
# Not show job search directly
```

### 2. Test Resume Upload:
- Signup → Login
- Click "Upload Resume"
- Upload a PDF/DOCX resume
- Check: `uploads/resumes/` folder has your file

### 3. Test Job Search:
- Search for "python developer" in "New York"
- Should see jobs
- If resume uploaded: See match scores!

### 4. Test Match Scores:
- After uploading resume
- Search jobs
- Look for badges like: 🎯 85% Match
- See matched skills below job title

---

## 📊 View Database

### Using SQLite:
```bash
sqlite3 job_search.db

# View tables
.tables

# View users
SELECT * FROM users;

# View resumes
SELECT id, user_id, filename, years_experience FROM resumes;

# Exit
.quit
```

### Using DB Browser (GUI):
- Download: https://sqlitebrowser.org
- Open: `job_search.db`

---

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python run.py --port 5001
```

### Issue: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Database error
```bash
# Delete and recreate database
rm job_search.db
python run.py
# Database auto-creates
```

### Issue: Resume parsing fails
```bash
# Install missing libraries
pip install PyPDF2 python-docx pdfplumber
```

### Issue: Can't see match scores
**Solution:**
1. Make sure you're logged in
2. Upload a resume first
3. Search for jobs
4. Match scores appear on job cards

---

## 📁 File Structure

```
.
├── run.py                      # Main entry point
├── requirements.txt            # All dependencies
├── job_search.db              # SQLite database (auto-created)
├── job_search_app/            # Main application
│   ├── models/                # Database models
│   ├── routes/                # API routes
│   ├── services/              # Business logic
│   ├── templates/             # HTML pages
│   └── static/                # CSS/JS
└── uploads/                   # Uploaded files (auto-created)
    └── resumes/               # User resumes
```

---

## ✨ Features Available Locally

### Without Resume:
- ✅ Search jobs from Indeed, LinkedIn
- ✅ Scrape 24 trading firms
- ✅ View job details
- ✅ Download CSV results

### With Resume:
- ✅ All above features
- ✅ **AI match scores** on every job
- ✅ **Skills breakdown**
- ✅ **Color-coded badges**
- ✅ **Jobs sorted by match**

---

## 🚀 Quick Demo Account

**For Testing:**
```
Email: test@example.com
Username: testuser
Password: test123456
Full Name: Test User
```

Upload a sample resume, then search!

---

## 💡 Tips

### Speed up searches:
- Use "results_wanted: 5" for quick tests
- Use "Indeed" only (faster than LinkedIn)

### Test AI matching:
- Upload a tech resume with clear skills
- Search "python developer"
- Should see high match scores for Python jobs

### Test without resume:
- Create account but DON'T upload resume
- Search jobs
- Should work normally, no match scores

---

## 📞 Need Help?

**Check logs:**
```bash
tail -50 job_search_app.log
```

**Check database:**
```bash
sqlite3 job_search.db "SELECT COUNT(*) FROM users;"
```

**Restart fresh:**
```bash
rm job_search.db
rm -rf uploads/
python run.py
```

---

## 🎉 Success Checklist

- [ ] App starts without errors
- [ ] Can access http://localhost:5000
- [ ] Redirects to login page
- [ ] Can create account
- [ ] See splash screen after login
- [ ] Dashboard loads
- [ ] Can upload resume
- [ ] Can search jobs
- [ ] See match scores (after resume upload)

---

**Enjoy your AI-powered job search platform!** 🚀
