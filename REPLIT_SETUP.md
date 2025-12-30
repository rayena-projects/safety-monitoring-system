# Replit Deployment Guide

## Quick Setup (5 minutes)

This guide will help you create a **live, interactive demo** of the Personal Safety Monitoring System that anyone can access from their browser.

---

## Step 1: Create a Replit Account

1. Go to [replit.com](https://replit.com)
2. Sign up for a free account (or log in if you have one)
3. Verify your email

---

## Step 2: Create a New Repl

### Option A: Import from GitHub (Recommended)

1. Click **"+ Create"** button in Replit dashboard
2. Select **"Import from GitHub"**
3. Enter your GitHub repository URL:
   ```
   https://github.com/yourusername/safety-monitoring-system
   ```
4. Click **"Import from GitHub"**
5. Replit will automatically detect it's a Python project

### Option B: Manual Upload

1. Click **"+ Create"** button
2. Select **"Python"** as the template
3. Name your Repl: `safety-monitoring-system`
4. Click **"Create Repl"**
5. Delete the default `main.py` file
6. Upload all your project files:
   - Drag and drop all `.py` files
   - Or use the "Upload file" button in the file explorer

---

## Step 3: Verify Files

Make sure these files are present in your Repl:

```
.
├── .replit               # Replit configuration (tells it to run main.py)
├── replit.nix            # Environment configuration
├── main.py               # Entry point
├── health_monitor.py     # Core monitoring logic
├── sensor_reading.py     # Data models
├── sensor_simulator.py   # Sensor simulation
├── baseline_data.py      # Baseline storage
├── alert_system.py       # Alert notifications
├── ui_utils.py           # Terminal UI
├── demo_ui.py            # UI demonstration
├── README.md             # Documentation
└── ARCHITECTURE.md       # Architecture docs
```

---

## Step 4: Test the Application

1. Click the big green **"Run"** button at the top
2. The application should start in the console
3. You'll see the welcome screen:
   ```
   ════════════════════════════════════════════════════════
             PERSONAL SAFETY MONITORING SYSTEM
   ════════════════════════════════════════════════════════
   ```

4. Follow the prompts:
   - Enter baseline heart rate (or press Enter for default 75)
   - Optionally set up a PIN
   - Press Enter to begin monitoring

---

## Step 5: Share Your Live Demo

### Get Your Shareable Link

1. After the Repl runs successfully, look for the URL at the top
2. It will be something like:
   ```
   https://replit.com/@yourusername/safety-monitoring-system
   ```

3. Click the **"Share"** button (icon looks like a chain link)
4. Copy the **"Invite link"**
5. This link allows anyone to:
   - View your code
   - Run the application in their browser
   - Interact with the monitoring system

### Update Your README

Add the Replit link to your README.md:

```markdown
## 📺 Demo

### Live Interactive Demo
Try the system yourself: **[Run on Replit →](https://replit.com/@yourusername/safety-monitoring-system)**
```

---

## Step 6: Make It Public (For College Applications)

1. Click the **three dots (⋮)** next to your Repl name
2. Select **"Repl settings"**
3. Under **"Privacy"**, select **"Public"**
4. Click **"Save"**

Now anyone with the link can see and run your project!

---

## Troubleshooting

### Issue: Colors Don't Display Properly

**Solution**: Replit's console supports ANSI colors, but if you see weird characters:
- The colors should still work fine
- Try using the "Shell" tab instead of "Console"

### Issue: Timeout Not Working

**Problem**: `signal.alarm()` may not work in Replit's environment

**Solution**: This is expected - the simulation will still run, but the 15-second timeout might not work. Add a note in your demo:

```python
# Note for Replit users
print("Note: Running in browser environment - timeouts may not function")
```

### Issue: CTRL+C Doesn't Work

**Solution**: In Replit, use the "Stop" button instead of CTRL+C to end monitoring.

---

## Advanced: Embedding in Website

You can embed your Repl in a website or portfolio:

```html
<iframe
  src="https://replit.com/@yourusername/safety-monitoring-system?embed=true"
  width="800"
  height="600"
  frameborder="0">
</iframe>
```

---

## For College Applications

### How to Present This

1. **In Your Application**:
   ```
   Live Demo: https://replit.com/@yourusername/safety-monitoring-system

   Click "Run" to see the system in action. The demo simulates
   drink spiking detection through heart rate monitoring.
   ```

2. **In Your Resume/Portfolio**:
   ```
   Personal Safety Monitoring System
   • Python-based wearable safety technology
   • Live demo: replit.com/@yourusername/safety-monitoring-system
   • GitHub: github.com/yourusername/safety-monitoring-system
   ```

3. **Advantages of Replit Demo**:
   - ✅ Admissions officers can try it **instantly** (no installation)
   - ✅ Works on any device (even smartphones)
   - ✅ Shows you know modern deployment practices
   - ✅ Demonstrates the code is real and functional

---

## Alternative: Replit Teams for Education

If you're a student, you can use **Replit Teams for Education**:

1. Join with your school email
2. Get access to better hardware
3. Private repls with better sharing controls
4. Multiplayer coding (good for demonstrating collaboration)

Sign up: [replit.com/teams-for-education](https://replit.com/teams-for-education)

---

## Next Steps After Replit Setup

1. ✅ Update README.md with your Replit link
2. ✅ Test the demo thoroughly
3. ✅ Create a demo video (see DEMO_VIDEO_GUIDE.md)
4. ✅ Add screenshots to README
5. ✅ Share on LinkedIn/portfolio

---

## Tips for Best Demo Experience

### 1. Add Instructions at the Top

Edit `main.py` to add browser-specific instructions:

```python
def main():
    # Detect if running in Replit
    import os
    if os.environ.get('REPL_ID'):
        print("🌐 Running in Replit browser environment")
        print("📝 Use the 'Stop' button to end monitoring (CTRL+C may not work)")
        print()
```

### 2. Reduce Delays for Faster Demo

For Replit, you might want faster cycles:

```python
# In health_monitor.py - Optional: faster demo mode
CYCLE_DELAY = 5  # Instead of 10 seconds
```

### 3. Add a Quick Demo Mode

Create `quick_demo.py` for a 30-second overview:

```python
"""Quick 30-second demo for Replit"""
from demo_ui import demo

if __name__ == "__main__":
    print("🎬 30-SECOND QUICK DEMO")
    print("=" * 60)
    demo()
    print("\n✨ Want to try the full monitoring system?")
    print("   Run 'main.py' instead!")
```

Update `.replit` to offer both:
```
run = "python3 main.py"
# Or for quick demo: run = "python3 quick_demo.py"
```

---

## Security Note for Public Repls

Since your Repl is public:

- ✅ Don't include real phone numbers or personal data
- ✅ Use dummy emergency contacts (already done)
- ✅ Don't commit API keys or secrets
- ✅ Add `.env` to `.gitignore` if you add environment variables

---

## Questions?

- **Replit Docs**: [docs.replit.com](https://docs.replit.com)
- **Replit Community**: [replit.com/community](https://replit.com/community)
- **Python on Replit**: [docs.replit.com/programming-ide/getting-started-python](https://docs.replit.com/programming-ide/getting-started-python)

---

**Congratulations!** 🎉 You now have a live, shareable demo that runs in any browser. This is a powerful addition to your college applications!
