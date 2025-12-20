# Job Search App - Control Scripts

## Quick Commands

### Start/Restart the App
```bash
./start_app.sh
```
or
```bash
./restart_app_clean.sh
```
**This will:**
- Kill ALL old Python processes running the app
- Wait for processes to terminate
- Start a fresh new instance
- Verify the app is running
- Show you the URL and PID

### Stop the App
```bash
./stop_app.sh
```

### Check if App is Running
```bash
curl http://localhost:5000/health
```

### View Logs
```bash
tail -f job_search_app.log
```

### View Last 50 Log Lines
```bash
tail -50 job_search_app.log
```

## Run Manually (with auto-cleanup)
```bash
python run.py
```
This now automatically kills old instances before starting!

## Troubleshooting

### Port Already in Use
The scripts handle this automatically, but if needed:
```bash
lsof -ti:5000 | xargs kill -9
```

### Find Running Processes
```bash
ps aux | grep "python run.py"
```

### Kill All Python Processes (Nuclear Option)
```bash
pkill -9 python
```
⚠️ Warning: This kills ALL Python processes!

## Files Created
- `restart_app_clean.sh` - Clean restart script
- `start_app.sh` - Quick start command
- `stop_app.sh` - Stop the app
- `run.py` - Main entry point (now auto-kills old instances)
