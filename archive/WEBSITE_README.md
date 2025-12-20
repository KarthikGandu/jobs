# 🚀 Karthik's Job Search Site

A beautiful, fast, and modern web application to search for jobs across multiple platforms including Indeed, LinkedIn, Glassdoor, ZipRecruiter, and Google Jobs.

## ✨ Features

### 🎯 Multi-Site Search
- **Indeed** (default - no LinkedIn default as requested)
- **LinkedIn**
- **Glassdoor**
- **ZipRecruiter**
- **Google Jobs**

### 🔍 Advanced Filters
- **Multiple Search Terms**: Add multiple job titles/keywords
- **Job Type**: Full-time, Part-time, Contract, Internship
- **Remote Work**: Filter for remote positions
- **Location-based**: Search by city, state, or country
- **Distance Radius**: Customize search radius (miles)
- **Posted Date**: Filter by hours old (24h, 3 days, week, month)
- **LinkedIn Experience Level**: Internship, Entry Level, Associate, Mid-Senior, Director, Executive

### ⚡ Optimized Performance
- **Fast Scraping**: Reduced sleep times for quicker results
- **Parallel Processing**: Searches multiple sites simultaneously
- **Real-time Loading**: Creative loading indicators with progress updates
- **Immediate Results**: Jobs display as soon as fetched

### 💾 Export Options
- Download results as CSV
- Unique filename generation with timestamps
- All job details included

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install flask flask-cors pandas
   ```

2. **Run the Application**
   ```bash
   # Option 1: Using the startup script
   ./run_app.sh

   # Option 2: Direct Python command
   python3 app.py
   ```

3. **Access the Website**
   Open your browser and navigate to:
   ```
   http://localhost:5001
   ```

## 📖 How to Use

### Basic Search
1. Enter job title(s) or keywords (press Enter to add multiple)
2. Enter location (e.g., "New York", "Remote", "USA")
3. Select one or more job sites (Indeed is pre-selected)
4. Click "Search Jobs"

### Advanced Search
1. Click "Advanced Filters" to expand more options
2. Select job type(s) from the dropdown (hold Ctrl/Cmd for multiple)
3. Check "Remote Jobs Only" if you want only remote positions
4. For LinkedIn searches, select experience levels
5. Adjust "Results per Site" (default: 20)
6. Set distance radius in miles (default: 50)
7. Filter by posting date (optional)

### Example Searches

**Software Engineer in San Francisco**
```
Job Title: Software Engineer
Location: San Francisco, CA
Sites: Indeed, LinkedIn, Glassdoor
Job Type: Full-time
```

**Remote Data Analyst**
```
Job Title: Data Analyst
Location: Remote
Sites: Indeed, ZipRecruiter, Google
Remote: Yes
Results: 30 per site
```

**Entry Level Positions**
```
Job Title: Junior Developer, Entry Level Engineer
Location: New York, NY
Sites: LinkedIn, Indeed
Experience Level: Internship, Entry Level
Posted Within: Last week
```

## 🎨 Design Features

- **Modern UI**: Clean, professional gradient background
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Color-coded Sites**: Each job site has its own color scheme
- **Smooth Animations**: Cards, buttons, and transitions
- **Icon Integration**: Font Awesome icons throughout
- **Loading States**: Engaging spinners and progress messages
- **Interactive Cards**: Hover effects and clickable job links

## 📊 Job Card Information

Each job result displays:
- **Job Title** (clickable link to original posting)
- **Company Name**
- **Location**
- **Date Posted**
- **Salary Range** (if available)
- **Job Type** (Full-time, Part-time, etc.)
- **Remote Badge** (if applicable)
- **Experience Level** (if available)
- **Site Source** (color-coded badge)
- **Brief Description** (if available)

## 🔧 Configuration

### Backend (app.py)
- **Port**: Default 5000 (change in `app.run()`)
- **Host**: Default 0.0.0.0 (accessible from network)
- **Output Directory**: `job_results/` (auto-created)

### Scraping Settings
The application uses optimized settings for fast results:
- No artificial sleep delays between API calls
- Parallel processing for multiple sites
- Efficient data handling with pandas

## 📁 Project Structure

```
.
├── app.py                 # Flask backend API
├── templates/
│   └── index.html        # Main HTML page
├── static/
│   ├── style.css         # Styling and animations
│   └── script.js         # Frontend logic
├── job_results/          # Downloaded CSV files
├── requirements.txt      # Python dependencies
├── run_app.sh           # Startup script
└── WEBSITE_README.md    # This file
```

## 🚨 Troubleshooting

### Application won't start
- Ensure all dependencies are installed: `pip install flask flask-cors pandas`
- Check if port 5001 is available: `lsof -i :5000`
- Verify Python version: `python3 --version`

### No results found
- Check your internet connection
- Try different search terms
- Increase "Results per Site"
- Remove date filters
- Try different job sites

### Slow performance
- Reduce "Results per Site"
- Search fewer sites at once
- Check network speed
- Disable "Fetch Description" if enabled

## 🔐 Privacy & Data

- All scraping is done server-side
- No personal data is collected
- Job data is stored locally in CSV format
- Results are temporary and can be deleted anytime

## 📝 Footer

The site footer includes:
- Copyright notice with current year (© 2025 Karthik)
- "Powered by JobSpy2 & Modern Web Technologies"

## 🎯 Tips for Best Results

1. **Use Multiple Search Terms**: Add variations of job titles
2. **Cast a Wide Net**: Select multiple job sites
3. **Be Specific with Location**: Use city names for better results
4. **Use Filters Wisely**: Too many filters may limit results
5. **Try Different Sites**: Each platform has different listings
6. **Check Remote Options**: Many jobs offer remote work
7. **Download CSV**: Save results for later review

## 🔄 Updates & Maintenance

The application automatically:
- Creates unique filenames for each search
- Handles errors gracefully
- Removes duplicate job listings
- Sorts results by site and date

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure the backend is running on port 5001
4. Check browser console for JavaScript errors

---

**Built with ❤️ by Karthik**

*Leveraging JobSpy2 library for powerful job scraping capabilities*
