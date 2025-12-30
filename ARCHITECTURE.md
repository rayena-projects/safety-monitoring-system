# System Architecture

## Overview

The Personal Safety Monitoring System follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                           │
│                                                                   │
│  ┌──────────────┐              ┌────────────────────┐           │
│  │   main.py    │              │   ui_utils.py      │           │
│  │              │──────────────│                    │           │
│  │ • User Setup │              │ • Colors           │           │
│  │ • PIN Config │              │ • Status Boxes     │           │
│  └──────────────┘              │ • Progress Bars    │           │
│                                 │ • Gauges           │           │
│                                 └────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                        │
│                                                                   │
│  ┌─────────────────────────────────────────────────────┐        │
│  │            health_monitor.py                         │        │
│  │                                                       │        │
│  │  ┌───────────────────────────────────────┐          │        │
│  │  │      State Machine                    │          │        │
│  │  │                                        │          │        │
│  │  │  • awaiting_user_response             │          │        │
│  │  │  • user_previously_said_safe          │          │        │
│  │  │  • consecutive_abnormal_after_yes     │          │        │
│  │  │  • alert_sent                         │          │        │
│  │  │  • last_abnormality                   │          │        │
│  │  └───────────────────────────────────────┘          │        │
│  │                                                       │        │
│  │  Core Methods:                                       │        │
│  │  • start_monitoring()                                │        │
│  │  • _monitoring_loop()                                │        │
│  │  • _calculate_abnormality()                          │        │
│  │  • _prompt_user_safety()                             │        │
│  │  • _final_safety_check()                             │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
┌──────────────────┐ ┌────────────────┐ ┌──────────────────┐
│   DATA LAYER     │ │  SIMULATION    │ │  ALERT LAYER     │
│                  │ │     LAYER      │ │                  │
│ ┌──────────────┐ │ │ ┌────────────┐ │ │ ┌──────────────┐ │
│ │sensor_reading│ │ │ │sensor_     │ │ │ │alert_system  │ │
│ │    .py       │ │ │ │simulator   │ │ │ │    .py       │ │
│ │              │ │ │ │    .py     │ │ │ │              │ │
│ │ • heart_rate │ │ │ │            │ │ │ │ • Contacts   │ │
│ │ • motion     │ │ │ │ • Weighted │ │ │ │ • send_alert │ │
│ └──────────────┘ │ │ │   random   │ │ │ └──────────────┘ │
│                  │ │ │ • HR ranges│ │ │                  │
│ ┌──────────────┐ │ │ └────────────┘ │ │  In Production:  │
│ │baseline_data │ │ │                │ │  ↓               │
│ │    .py       │ │ │ In Production: │ │  • Twilio SMS    │
│ │              │ │ │  ↓             │ │  • FCM Push      │
│ │ • Baseline   │ │ │  • Apple Watch │ │  • Email         │
│ │   heart rate │ │ │  • Fitbit API  │ │  • 911 API       │
│ └──────────────┘ │ │  • BLE HRM     │ │                  │
└──────────────────┘ └────────────────┘ └──────────────────┘
```

---

## Data Flow Diagram

### Monitoring Cycle Flow

```
START
  │
  ▼
┌─────────────────────────┐
│ User Configuration      │
│ • Baseline HR           │
│ • Optional PIN          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Initialize Monitor      │
│ • Create AlertSystem    │
│ • Reset state variables │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Monitoring Loop Start   │
│ Cycle N                 │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Collect Sensor Reading  │
│ • HR: 40-130 bpm        │
│ • Motion: true/false    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Add to Sliding Window   │
│ Keep last 5 readings    │
└───────────┬─────────────┘
            │
            ▼
     ┌──────┴──────┐
     │ Cycle 1-4?  │
     └──────┬──────┘
        YES │  NO
            │  │
            │  ▼
            │  ┌─────────────────────────┐
            │  │ Calculate Abnormality   │
            │  │ • Only if HR<50 or >80  │
            │  │ • AND no motion         │
            │  │ • Score: 0-100          │
            │  └────────────┬────────────┘
            │               │
            │               ▼
            │        ┌──────┴──────────┐
            │        │ Abnormality     │
            │        │   > 45%?        │
            │        └──────┬──────────┘
            │           YES │  NO
            │               │  │
            │               │  └────┐
            │               ▼       │
            │        ┌─────────────────────────┐
            │        │ Check State Machine     │
            │        │                         │
            │        │ awaiting_response?      │
            │        │  ├─YES→ Ask again       │
            │        │  └─NO→                  │
            │        │                         │
            │        │ user_said_safe?         │
            │        │  ├─NO→ First time,      │
            │        │  │     prompt user      │
            │        │  └─YES→                 │
            │        │     Sharp jump>20%?     │
            │        │      ├─YES→ Ask now     │
            │        │      └─NO→              │
            │        │        3 consecutive?   │
            │        │         ├─YES→ Ask now  │
            │        │         └─NO→ Continue  │
            │        └────────────┬────────────┘
            │                     │
            │                     ▼
            │              ┌──────────────┐
            │              │ Prompt User  │
            │              │ 15s timeout  │
            │              └──────┬───────┘
            │                     │
            │                     ▼
            │              ┌──────┴────────┐
            │              │ User Response?│
            │              └──────┬────────┘
            │                YES  │  NO/TIMEOUT
            │                     │  │
            │      ┌──────────────┘  │
            │      ▼                 ▼
            │  ┌────────┐     ┌──────────┐
            │  │ Safe!  │     │ Alert!   │
            │  │ Track  │     │ Send to  │
            │  │consecutive   │ contacts │
            │  └────┬───┘     └────┬─────┘
            │       │              │
            └───────┴──────────────┴────────┐
                                             │
                    ┌────────────────────────┘
                    │
                    ▼
            ┌──────────────┐
            │ Delay 10s    │
            │ or REMOVE    │
            └──────┬───────┘
                   │
                   ▼
            ┌──────┴──────┐
            │ Continue?   │
            └──────┬──────┘
               YES │  NO
                   │  │
                   │  ▼
                   │  ┌─────────────────┐
                   │  │ Final Safety    │
                   │  │ Check           │
                   │  └────────┬────────┘
                   │           │
                   │           ▼
                   │         END
                   │
                   └──────────┐
                              │
                (Loop back to Cycle N+1)
```

---

## State Machine Diagram

### Safety Response State Machine

```
                    ┌─────────────────┐
                    │  NORMAL STATE   │
                    │                 │
                    │ abnormality     │
                    │   0-45%         │
                    └────────┬────────┘
                             │
                             │ abnormality > 45%
                             │ (first time)
                             ▼
                    ┌─────────────────┐
                    │ PROMPTED STATE  │
                    │                 │
                    │ Waiting for     │
                    │ user response   │
                    └────┬───────┬────┘
                         │       │
                    YES  │       │  NO/TIMEOUT
                         │       │
                         ▼       ▼
              ┌──────────────┐ ┌─────────────────┐
              │ TRACKING     │ │ AWAITING        │
              │ STATE        │ │ RESPONSE STATE  │
              │              │ │                 │
              │ user_said_   │ │ alert_sent=true │
              │ safe=true    │ │ awaiting=true   │
              │ consecutive  │ │                 │
              │ counter=0    │ │ Next cycle:     │
              └───────┬──────┘ │ ask again       │
                      │        └─────────────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      │ abnormal      │ normal        │ sharp jump
      │ cycle         │ cycle         │ >20%
      ▼               ▼               ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ counter  │    │ RESET to │    │ ASK      │
│ ++       │    │ NORMAL   │    │ NOW      │
└────┬─────┘    │ STATE    │    └────┬─────┘
     │          └──────────┘         │
     │                               │
     │ counter=3?                    │
     │    YES                        │
     └─────────┬─────────────────────┘
               │
               ▼
        ┌─────────────┐
        │ Prompt User │
        │ Again       │
        └──────┬──────┘
               │
        ┌──────┴──────┐
        │             │
     YES│             │NO/TIMEOUT
        │             │
        ▼             ▼
   ┌─────────┐  ┌──────────┐
   │ RESET   │  │ SEND     │
   │ counter │  │ ALERT    │
   │ to 0    │  │          │
   └─────────┘  └──────────┘
```

---

## Component Interaction Diagram

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │ Configures (HR, PIN)
       ▼
┌─────────────────────────────────────────┐
│           main.py                        │
│                                          │
│  1. Collect configuration                │
│  2. Validate input                       │
│  3. Display summary                      │
└──────────┬───────────────────────────────┘
           │ Instantiates
           ▼
┌─────────────────────────────────────────┐
│       HealthMonitor                      │
│                                          │
│  start_monitoring()                      │
└───┬──────────────────────────┬──────────┘
    │                          │
    │ Uses                     │ Uses
    ▼                          ▼
┌──────────────┐      ┌──────────────────┐
│ UI           │      │  AlertSystem     │
│              │      │                  │
│ • header()   │      │  • send_alert()  │
│ • gauge()    │      └──────────────────┘
│ • status()   │
└───┬──────────┘
    │ Uses
    ▼
┌──────────────┐
│ Colors       │
│              │
│ ANSI codes   │
└──────────────┘

┌──────────────────────────────────────────┐
│      _monitoring_loop()                  │
└───┬──────────────────────────────────────┘
    │ Calls every cycle
    ▼
┌──────────────────────────────────────────┐
│   SensorSimulator.generate_reading()     │
│                                          │
│   Returns SensorReading(hr, motion)     │
└───┬──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│   last_five_readings.append(reading)     │
│   Maintain sliding window                │
└───┬──────────────────────────────────────┘
    │
    │ If cycle >= 5
    ▼
┌──────────────────────────────────────────┐
│   _calculate_abnormality(readings)       │
│                                          │
│   Returns: 0-100 score                   │
└───┬──────────────────────────────────────┘
    │
    │ If abnormality > 45%
    ▼
┌──────────────────────────────────────────┐
│   _prompt_user_safety()                  │
│                                          │
│   • signal.alarm(15)                     │
│   • input() with timeout                 │
│   • Validate PIN if enabled              │
│   Returns: bool (safe or not)            │
└───┬──────────────────────────────────────┘
    │
    │ If unsafe or timeout
    ▼
┌──────────────────────────────────────────┐
│   alert_system.send_alert()              │
│                                          │
│   In production: Twilio/FCM/Email        │
└──────────────────────────────────────────┘
```

---

## Technology Stack

### Current Implementation (Simulation)

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.7+ | Core implementation |
| **UI** | ANSI escape codes | Terminal colors and formatting |
| **Timeout** | UNIX signals (SIGALRM) | Non-blocking input with timeout |
| **Data Structures** | Lists, typing module | Sliding window, type hints |
| **Simulation** | random module | Sensor data generation |

### Production Architecture (Future)

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Sensors** | Apple HealthKit / Fitbit API | Real heart rate and motion data |
| **Backend** | Python FastAPI / Flask | REST API for monitoring |
| **Database** | PostgreSQL + TimescaleDB | Time-series health data |
| **Caching** | Redis | Real-time state management |
| **Alerts** | Twilio (SMS), FCM (push) | Emergency notifications |
| **Frontend** | React Native / Swift | Mobile app interface |
| **Hosting** | AWS / Google Cloud | Cloud infrastructure |
| **ML** | scikit-learn / TensorFlow | Personalized anomaly detection |

---

## Security Architecture

### Current Implementation

```
┌─────────────────────────────────────────┐
│         Security Features                │
├─────────────────────────────────────────┤
│                                          │
│  1. PIN Authentication                   │
│     • 4-6 digit PIN                      │
│     • Validates on YES/REMOVE commands   │
│     • Incorrect PIN = no response        │
│                                          │
│  2. Local Processing                     │
│     • All data stays on device           │
│     • No cloud transmission              │
│     • Privacy-first design               │
│                                          │
│  3. Timeout Protection                   │
│     • 15s response window                │
│     • Prevents indefinite blocking       │
│     • Auto-escalates on timeout          │
│                                          │
└─────────────────────────────────────────┘
```

### Production Security Requirements

```
┌─────────────────────────────────────────┐
│       Production Security                │
├─────────────────────────────────────────┤
│                                          │
│  1. Data Encryption                      │
│     • AES-256 for data at rest           │
│     • TLS 1.3 for data in transit        │
│     • End-to-end encryption for alerts   │
│                                          │
│  2. Authentication                       │
│     • OAuth 2.0 / JWT tokens             │
│     • Biometric authentication           │
│     • Multi-factor authentication        │
│                                          │
│  3. Compliance                           │
│     • HIPAA compliance (health data)     │
│     • GDPR compliance (EU users)         │
│     • SOC 2 Type II certification        │
│                                          │
│  4. Access Control                       │
│     • Role-based access (RBAC)           │
│     • Emergency contact verification     │
│     • Audit logging                      │
│                                          │
└─────────────────────────────────────────┘
```

---

## Deployment Architecture (Future)

```
                         ┌──────────────┐
                         │   User's     │
                         │  Smartwatch  │
                         │              │
                         │ • HealthKit  │
                         │ • Bluetooth  │
                         └──────┬───────┘
                                │
                                │ HTTPS/WSS
                                ▼
┌───────────────────────────────────────────────────────┐
│                   Cloud Platform                       │
│                                                        │
│  ┌──────────────┐        ┌────────────────┐          │
│  │  API Gateway │        │  Load Balancer │          │
│  └──────┬───────┘        └───────┬────────┘          │
│         │                        │                    │
│         ▼                        ▼                    │
│  ┌──────────────────────────────────────┐            │
│  │     Application Layer (Kubernetes)    │            │
│  │                                        │            │
│  │  ┌────────────┐    ┌──────────────┐  │            │
│  │  │ Monitoring │    │ Alert        │  │            │
│  │  │ Service    │───│  Service     │  │            │
│  │  └────────────┘    └──────────────┘  │            │
│  └────────────┬────────────────┬─────────┘            │
│               │                │                      │
│               ▼                ▼                      │
│  ┌─────────────────┐ ┌──────────────────┐            │
│  │   PostgreSQL    │ │  Redis Cache     │            │
│  │   TimescaleDB   │ │  State Machine   │            │
│  └─────────────────┘ └──────────────────┘            │
│                                                        │
│  External Services:                                   │
│  ┌──────────┐ ┌─────────┐ ┌────────────┐            │
│  │  Twilio  │ │   FCM   │ │  SendGrid  │            │
│  │   SMS    │ │  Push   │ │   Email    │            │
│  └──────────┘ └─────────┘ └────────────┘            │
└───────────────────────────────────────────────────────┘
```

---

## File Dependencies

```
main.py
├── health_monitor.py
│   ├── sensor_reading.py
│   ├── sensor_simulator.py
│   │   └── sensor_reading.py
│   ├── alert_system.py
│   │   └── ui_utils.py
│   └── ui_utils.py
└── ui_utils.py

demo_ui.py
└── ui_utils.py

baseline_data.py (standalone)
```

---

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Cycle Interval** | 10 seconds | Configurable via CYCLE_DELAY |
| **Response Timeout** | 15 seconds | Configurable via RESPONSE_TIMEOUT |
| **Sliding Window** | 5 readings | 50 seconds of history |
| **Memory Usage** | ~5 MB | Minimal - standard library only |
| **CPU Usage** | <1% | Simple calculations |
| **Latency** | <100ms | From reading to display |

---

## Error Handling Strategy

```
┌─────────────────────────────────────────┐
│          Error Scenarios                 │
├─────────────────────────────────────────┤
│                                          │
│  1. User Timeout                         │
│     → Treat as unsafe                    │
│     → Send alert                         │
│                                          │
│  2. Incorrect PIN                        │
│     → Treat as no response               │
│     → Send alert                         │
│                                          │
│  3. KeyboardInterrupt (CTRL+C)           │
│     → Perform final safety check         │
│     → Graceful exit                      │
│                                          │
│  4. REMOVE Command                       │
│     → Perform final safety check         │
│     → SystemExit                         │
│                                          │
│  5. Signal Errors (Windows)              │
│     → Fallback to no timeout             │
│     → Log warning                        │
│                                          │
└─────────────────────────────────────────┘
```
