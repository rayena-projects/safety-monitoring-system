<div align="center">

# Personal Safety Monitoring System

### AI-Powered Wearable Safety Technology for Drink Spiking Detection

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-professional-brightgreen.svg)](https://github.com/psf/black)
[![Platform](https://img.shields.io/badge/platform-Unix%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/)

[Live Demo](#-demo) • [Features](#-features) • [Installation](#-installation) • [Documentation](#-how-it-works) • [Architecture](#-architecture)

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Demo](#-demo)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [Technical Details](#-technical-details)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

---

## 🎯 Overview

The **Personal Safety Monitoring System** is an intelligent wearable health monitoring solution designed to detect potential drink spiking incidents through physiological anomaly detection. By continuously analyzing heart rate and motion data, the system can identify concerning patterns and automatically alert emergency contacts when intervention may be needed.

### Primary Use Case
Detecting drink spiking through physiological changes—specifically monitoring for heart rate abnormalities (bradycardia or tachycardia) while the user remains stationary, which can indicate incapacitation.

### Why This Matters
- **1 in 13** women and **1 in 24** men experience drink spiking in their lifetime
- Early detection can enable timely intervention and prevent assault
- Automated monitoring provides protection when the victim cannot self-advocate

---

## 📺 Demo

> **Note**: Demo materials will be added here

### Live Interactive Demo
Try the system yourself: **[Run on Replit →](https://replit.com/@rayenajjwala/safety-monitoring-system?v=1)**

*👆 Click to run the full monitoring system in your browser (no installation required!)*

### Video Walkthrough
Watch a 2-minute demonstration of the system in action:

**[▶️ View Demo Video on YouTube](https://youtube.com/watch?v=your-video-id)**


### Visual Preview
![System Demo](demo.gif)


---

## ✨ Features

### Core Functionality
- **Real-time Physiological Monitoring**: Continuous heart rate and motion sensor tracking
- **Intelligent Anomaly Detection**: ML-inspired scoring algorithm that flags abnormalities only when clinically relevant (HR <50 or >80 bpm with no motion)
- **Graduated Response System**: Multi-level escalation with user confirmation before alerting
- **Automated Emergency Alerts**: Immediate notification to pre-configured emergency contacts
- **Final Safety Check**: Always verifies user safety before ending monitoring session

### Security & Privacy
- **Optional PIN Protection**: 4-6 digit PIN prevents unauthorized safety confirmations or watch removal
- **Secure Response Format**: PIN-validated commands (`YES 1234`, `REMOVE 1234`)
- **Privacy-First Design**: All data processing happens locally, no cloud transmission

### Smart Detection Algorithms
- **Consecutive Cycle Tracking**: Asks for confirmation after 3 consecutive abnormal readings
- **Sharp Jump Detection**: Immediate check-in if abnormality increases >20% suddenly
- **Baseline Calibration**: Personalized to each user's resting heart rate
- **Motion Context Awareness**: Only flags heart rate issues when user is stationary

### User Experience
- **Enhanced Visual Interface**: Color-coded terminal output with ANSI styling
- **Real-time Progress Indicators**: Visual gauges for abnormality levels
- **Status Dashboard**: Configuration summary boxes and monitoring settings
- **Responsive Timeout System**: 15-second safety check windows with clear prompts

---

## 🏗 Architecture

📖 **[View Detailed Architecture Documentation →](ARCHITECTURE.md)**

The architecture document includes:
- Complete system diagrams with data flow
- State machine visualizations
- Component interaction diagrams
- Production deployment architecture
- Security architecture
- Technology stack details

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│              (Entry Point & Configuration)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    health_monitor.py                         │
│           (Core Monitoring Logic & State Machine)            │
└───────┬────────────────────┬───────────────────┬────────────┘
        │                    │                   │
        ▼                    ▼                   ▼
┌───────────────┐   ┌──────────────────┐   ┌──────────────┐
│sensor_reading │   │ sensor_simulator │   │alert_system  │
│     .py       │   │      .py         │   │    .py       │
│ (Data Model)  │   │ (Data Generator) │   │(Notifications)│
└───────────────┘   └──────────────────┘   └──────────────┘
        │                    │                   │
        └────────────────────┴───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   ui_utils.py   │
                    │  (Visual Layer) │
                    └─────────────────┘
```

### Tech Stack
- **Language**: Python 3.7+
- **Core Libraries**: Standard library only (signal, time, typing, random)
- **UI Framework**: Custom ANSI terminal styling
- **Architecture Pattern**: Object-oriented with state machine pattern

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Unix/Linux/macOS (recommended for full timeout functionality)
- Windows (with limited timeout support)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/safety-monitoring-system.git
   cd safety-monitoring-system
   ```

2. **No dependencies to install!**
   This project uses only Python's standard library.

3. **Run the application**
   ```bash
   # On Unix/Linux/macOS
   python3 main.py

   # On Windows
   python main.py
   ```

4. **View the UI demo** (optional)
   ```bash
   python3 demo_ui.py
   ```

---

## 💻 Usage

### Initial Setup

When you first run the system, you'll configure:

1. **Baseline Heart Rate** (default: 75 bpm)
   - Enter your typical resting heart rate
   - System will use this to calibrate abnormality detection

2. **PIN Protection** (optional but recommended)
   - Create a 4-6 digit PIN for security
   - Format for responses: `YES 1234` or `REMOVE 1234`
   - Prevents unauthorized safety confirmations

### During Monitoring

The system will:
- Display real-time heart rate and motion data
- Show abnormality percentage with visual gauges
- Automatically ask "Are you okay?" when abnormality exceeds 45%
- Wait 15 seconds for your response

### Responding to Safety Checks

**Without PIN:**
- Type `YES` to confirm you're safe
- Type `REMOVE` to end monitoring

**With PIN:**
- Type `YES [PIN]` (e.g., `YES 1234`) to confirm safety
- Type `REMOVE [PIN]` to end monitoring

### Ending the Session

- Type `REMOVE` (+ PIN if enabled) during any prompt
- Or press `CTRL+C` to interrupt
- System will always perform a final safety check before terminating

---

## 🔬 How It Works

### Phase 1: Initial Data Collection (Cycles 1-4)
- System collects baseline readings
- Abnormality always shows 0% during this phase
- Progress bar indicates data collection status

### Phase 2: Active Monitoring (Cycle 5+)

#### Abnormality Calculation
Abnormality is flagged **ONLY** when:
- Heart rate < 50 bpm (bradycardia) **OR** > 80 bpm (tachycardia)
- **AND** no motion is detected (user is stationary)

The scoring algorithm analyzes a sliding window of 5 readings:
```python
# Simplified scoring logic
for reading in last_five_readings:
    if no_motion and (hr < 50 or hr > 80):
        if hr > 110: score += 25
        elif hr > 100: score += 20
        elif hr > 90: score += 15
        elif hr > 80: score += 10
        elif hr < 45: score += 20
        elif hr < 50: score += 10
```

#### Response Logic

**Abnormality 0-45%**: Normal status, monitoring continues

**Abnormality >45%**: System asks "Are you okay?"

- **First detection**: Immediate safety check
  - If YES → Track consecutive abnormal cycles (counter starts at 0)
  - If NO/no response → Send alert to emergency contacts

- **After user says "safe"**:
  - **Sharp jump detection**: If abnormality jumps >20% → Ask immediately
  - **Consecutive tracking**: Ask again after 3 consecutive abnormal cycles
  - If readings return to normal → Reset tracking

- **If no response was given**:
  - Next cycle → Ask again regardless of abnormality
  - If YES → Inform user that alert was sent, ask them to notify contacts
  - If NO/no response again → Send another alert

### Emergency Alert System

When triggered, the system sends notifications to:
- Mother - (123) 456-7890
- Father - (123) 456-7891
- Trusted Friend - (123) 456-7892

*Note: In production, these would be user-configured contacts with real SMS/call integration*

---

## ⚙️ Configuration

### Adjustable Parameters

Edit constants in [health_monitor.py](health_monitor.py):

```python
RESPONSE_TIMEOUT = 15      # Seconds to respond to safety check
CYCLE_DELAY = 10           # Gap between monitoring cycles
ESCALATION_THRESHOLD = 45  # Abnormality % to trigger user check
SHARP_JUMP_THRESHOLD = 20  # Abnormality % increase for immediate check
```

### Customizing Emergency Contacts

Update the contacts in [alert_system.py](alert_system.py):

```python
def send_alert(self):
    print(f"  ✓ Your Contact Name - (123) 456-7890")
```

---

## 🔧 Technical Details

### Project Structure

```
AutomatedSafetyMonitoringSystem/
├── main.py                 # Entry point with configuration UI
├── health_monitor.py       # Core monitoring state machine
├── sensor_reading.py       # Data class for sensor readings
├── sensor_simulator.py     # Weighted random data generator
├── baseline_data.py        # Baseline health metrics storage
├── alert_system.py         # Emergency contact notification
├── ui_utils.py             # Terminal UI utilities (colors, gauges)
├── demo_ui.py              # Standalone UI demonstration
└── README.md               # This file
```

### Key Algorithms

**State Machine Tracking:**
- `awaiting_user_response`: Waiting for delayed response
- `user_previously_said_safe`: Tracking consecutive abnormals after confirmation
- `consecutive_abnormal_after_yes`: Counter for abnormal cycles (0-indexed)
- `last_abnormality`: Previous cycle's score for jump detection

**Sensor Simulation:**
- 60% probability of no motion (realistic for sitting at bar/table)
- Weighted heart rate distribution:
  - 40% normal range (50-80 bpm)
  - 60% potentially abnormal (80-130 bpm or 40-50 bpm)

### Platform Compatibility

**Unix/Linux/macOS:**
- Full functionality including SIGALRM-based timeouts
- Recommended for production use

**Windows:**
- Core functionality works
- Timeout prompts may not function (SIGALRM not available)
- Consider using `msvcrt` module for Windows timeout implementation

---

## 🚀 Future Enhancements

### Planned Features
- [ ] **Actual Hardware Integration**: Connect to Fitbit/Apple Watch APIs
- [ ] **Machine Learning**: Personalized anomaly detection trained on user's historical data
- [ ] **Real SMS/Call Alerts**: Twilio integration for emergency notifications
- [ ] **GPS Location Sharing**: Send current location to emergency contacts
- [ ] **Web Dashboard**: Real-time monitoring interface for trusted contacts
- [ ] **Multi-language Support**: Internationalization for global deployment
- [ ] **Offline Data Storage**: SQLite database for health metrics history
- [ ] **False Positive Reduction**: Advanced filtering for exercise/stress scenarios

### Scalability Considerations
- Cloud-based monitoring dashboard
- Multi-user support with account management
- HIPAA-compliant data encryption
- Integration with emergency services (911 API)

---

## 🤝 Contributing

Contributions are welcome! This project is open to improvements in:
- Algorithm refinement for better accuracy
- Cross-platform compatibility (especially Windows timeout handling)
- Additional safety features
- UI/UX enhancements
- Documentation improvements

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see below for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Disclaimer

### Safety & Legal Notice

**This is a demonstration/educational project only.**

- This is **NOT** a medical device and should **NOT** be relied upon for actual safety monitoring
- This is **NOT** a substitute for professional safety measures or medical advice
- The creators assume **no liability** for any use of this software

### For Real Personal Safety Applications:
- Use certified safety devices and medical-grade sensors
- Consult with safety professionals and legal advisors
- Ensure proper user consent and privacy protection
- Follow local regulations regarding emergency alert systems
- Always have multiple safety measures in place

### Ethical Use
This project is designed for:
- **Educational purposes** to understand safety monitoring systems
- **Demonstration** of alert system logic and state machine patterns
- **Understanding** physiological monitoring concepts
- **Portfolio** demonstration for software engineering skills

### Privacy Considerations
In a real deployment, you must:
- Encrypt and securely store user health data
- Obtain consent from emergency contacts to receive alerts
- Implement clear privacy policies
- Comply with GDPR, HIPAA, or relevant data protection laws
- Provide users with data deletion and export capabilities

---

<div align="center">

**Built with ❤️ for safer social experiences**

[Report Bug](https://github.com/yourusername/safety-monitoring-system/issues) • [Request Feature](https://github.com/yourusername/safety-monitoring-system/issues)

</div>
