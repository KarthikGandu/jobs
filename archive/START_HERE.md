# 🚀 Quick Start Guide - Karthik's Job Search Site

## ⚡ Start the Application in 3 Steps

### Step 1: Install Dependencies (One-time setup)
```bash
pip install flask flask-cors pandas
```

### Step 2: Start the Server
```bash
# Easy way - Use the startup script
./run_app.sh

# OR direct Python command
python3 app.py
```

### Step 3: Open Your Browser
Go to: **http://localhost:5001**

---

## 🎯 Quick Demo Search

Try this example to get started:

1. **Add Job Title**: Type "Software Engineer" and press Enter
2. **Location**: Type "Remote" or "San Francisco"
3. **Select Sites**: Keep "Indeed" checked (default - fastest)
4. **Click**: "Search Jobs" button
5. **Wait**: 5-10 seconds for results
6. **Download**: Click "Download CSV" to save results

---

## 📋 Key Features Summary

✅ **Default Site**: Indeed (not LinkedIn as requested)  
✅ **Multiple Sites**: Indeed, LinkedIn, Glassdoor, ZipRecruiter, Google  
✅ **Fast Results**: Optimized with minimal delays  
✅ **Remote Filter**: Checkbox to filter remote jobs  
✅ **Job Types**: Full-time, Part-time, Contract, Internship  
✅ **Multiple Keywords**: Add several job titles  
✅ **Download**: Export to CSV with timestamp  
✅ **Real-time Loading**: Shows progress while fetching  
✅ **Beautiful UI**: Modern gradient design with animations  
✅ **Footer**: "© 2025 Karthik. All rights reserved."

---

## 🎨 Website Preview

**Header**: "Karthik's Job Search Engine" with briefcase icon  
**Subtitle**: "Find Your Dream Job Across Multiple Platforms"  
**Colors**: Blue/Purple gradient background, white cards  
**Footer**: Karthik's name with current year

---

## 📖 For More Details

See **WEBSITE_README.md** for:
- Complete feature list
- Advanced filtering options
- Troubleshooting guide
- Configuration options
- Example searches

---

## ⚠️ Important Notes

- **Port**: Application runs on port 5001
- **Results**: Displays up to 100 jobs per search in the UI
- **CSV**: Full results saved in `job_results/` folder
- **Speed**: Faster than CLI version (no sleep delays)
- **Default**: Indeed is pre-selected (no LinkedIn by default)

---

## 🎉 That's It!

You're ready to start searching for jobs!

**Made with ❤️ by Karthik**
