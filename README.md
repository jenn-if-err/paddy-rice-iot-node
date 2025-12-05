 Machine Learning and IOT-Based Paddy Rice Monitoring System

**Award:** **TOP 1 Best Paper** – Computing and Information Systems Category  
**Research In-House 2025** | Bohol Island State University - Main Campus

A machine learning and IoT-based paddy rice post-drying monitoring system that integrates real-time sensor data with predictive analytics to optimize rice yield tracking and moisture management across municipal, barangay, and farmer levels.

---

## Overview

**Paddy Rice Tracker** is an innovative **edge computing IoT system** designed to revolutionize post-harvest paddy rice management. Built for **Raspberry Pi 4**, this system combines embedded hardware sensors, local machine learning inference, and cloud synchronization to provide real-time monitoring and predictive analytics for rice quality control.


Implements an **offline-first architecture** with:
- **Edge AI inference** for instant predictions without internet dependency
- **IoT sensor integration** for automated environmental monitoring
- **Dual ML models** for moisture content and drying time prediction
- **Local-to-cloud synchronization** for centralized data analytics

---

## Cloud Integration

This edge node is designed to operate in tandem with the **Paddy Rice Tracker** for centralized data management and analytics.

### Cloud Platform Repository
🔗 [github.com/jenn-if-err/paddy_rice_tracker](https://github.com/jenn-if-err/paddy_rice_tracker)

### Key Integration Features
- **Automatic Data Sync**: Unsynced records automatically upload when internet is available
- **Centralized Dashboard**: Multi-farm analytics and reporting
- **User Management**: Cloud-based farmer and admin account management
- **Data Backup**: Redundant cloud storage for disaster recovery
- **API Gateway**: RESTful endpoints for mobile app integration

---

## The Team

* **Jennifer Tongco** – Team Leader, Lead Full-Stack Developer & System Architect
* **Claire Justin Pugio** – UI/UX Designer 
* **John Jabez Visarra** – Hardware Engineer & Frontend Support
* **John Kylo Cubelo** – Hardware Engineer
* **Engr. Jeralyn Alagon** – Thesis Adviser

---
## Key Features

### Machine Learning & Predictive Analytics
- **Moisture Content Prediction**: Random Forest Regressor model trained on capacitive sensor data, temperature, and humidity
- **Drying Time Estimation**: Multi-variable regression model predicting optimal drying duration based on initial moisture, target moisture, and environmental conditions
- **Real-Time Inference**: Sub-second prediction latency using pre-trained `scikit-learn` models with `joblib` serialization
- **Feature Scaling**: StandardScaler preprocessing for improved model accuracy

### IoT Hardware Integration
- **Multi-Sensor Array**: 
  - DHT22 temperature/humidity sensor
  - Capacitive soil moisture sensor (analog input)
  - Serial communication at 115200 baud rate
- **Arduino/ESP32 Firmware**: Custom C++ code for sensor polling and data transmission
- **PySerial Communication**: Robust USB serial interface with error handling and fallback mechanisms
- **Auto-Discovery**: Automatic port detection for Windows (`COM*`) and Linux (`/dev/ttyACM*`) systems

### Local Web Dashboard
- **Flask-based Interface**: Responsive web UI accessible at `localhost:5000`
- **Real-Time Monitoring**: Live sensor readings and prediction updates
- **Historical Records**: SQLite database for offline data persistence
- **User Management**: Multi-role authentication (Farmer, Barangay Admin, Municipal Admin)
- **Batch Management**: Track multiple drying batches with planting/harvesting dates

### Cloud Synchronization
- **RESTful API Integration**: Bidirectional sync with central cloud platform
- **Offline Queue**: Local storage of unsynced records during network outages
- **Token-Based Authentication**: Secure API communication using Bearer tokens
- **Batch Sync Operations**: Efficient bulk data transfer to minimize bandwidth

### Multi-Level Administration
- **Geographic Hierarchy**: Municipality → Barangay → Farmer organization
- **Role-Based Access Control**: Differentiated permissions for admins and farmers
- **Farmer Profiles**: Individual accounts linked to geographic locations
- **Aggregate Analytics**: Regional data insights for agricultural planning

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Edge Computing Node                      │
│                     (Raspberry Pi 4)                        │
│                                                             │
│  ┌────────────────┐      ┌──────────────────┐               │
│  │  Arduino/ESP32 │──USB──▶  PySerial      │              │
│  │  + DHT22       │      │  Interface       │               │
│  │  + Moisture    │      └─────────┬────────┘               │
│  │    Sensor      │                │                        │
│  └────────────────┘                ▼                        │
│                          ┌──────────────────┐               │
│                          │  Flask Web App   │               │
│                          │  (Local Server)  │               │
│                          └────────┬─────────┘               │
│                                   │                         │
│         ┌─────────────────────────┼─────────────────┐       │
│         ▼                         ▼                 ▼       │
│  ┌─────────────┐       ┌─────────────────┐  ┌──────────┐    │
│  │   ML Models │       │  SQLite Database│  │   Web UI │    │
│  │   (.joblib) │       │   (Local Store) │  │  (HTML)  │    │
│  └─────────────┘       └─────────────────┘  └──────────┘    │
│         │                         │                         │
└─────────┼─────────────────────────┼─────────────────────────┘
          │                         │
          └────────REST API─────────┘
                    │
                    ▼
          ┌──────────────────┐
          │  Cloud Platform  │
          │ (PostgreSQL DB)  │
          │   + Analytics    │
          └──────────────────┘
```

---

## Technology Stack

### Backend & Core Logic
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|----------|
| **Runtime** | Python | 3.11+ | Core application logic |
| **Web Framework** | Flask | 2.3.2 | Local web server & API |
| **ORM** | Flask-SQLAlchemy | 3.1.1 | Database abstraction |
| **Authentication** | Flask-Login | 0.6.2 | User session management |
| **Migration** | Flask-Migrate | 3.1.0 | Database schema versioning |

### Machine Learning & Data Science
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|----------|
| **ML Library** | Scikit-learn | 1.3.2 | Model training & inference |
| **Model Persistence** | Joblib | 1.3.2 | Model serialization |
| **Numerical Computing** | NumPy | 1.26.4 | Array operations |
| **Data Manipulation** | Pandas | 2.2.1 | DataFrame processing |

### Hardware & Communication
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|----------|
| **Serial Communication** | PySerial | 3.5 | Arduino/ESP32 interface |
| **HTTP Client** | Requests | 2.31.0 | Cloud API communication |

### Database & Deployment
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|----------|
| **Local Database** | SQLite | 3.x | Embedded data storage |
| **Cloud Database** | PostgreSQL | - | Production data store |
| **WSGI Server** | Gunicorn | 21.2.0 | Production deployment |
| **Cloud Platform** | Render | - | Web hosting service |

---

## Machine Learning Models

### 1. Moisture Content Prediction Model
- **Algorithm**: Random Forest Regressor
- **Input Features**: 
  - Capacitive sensor reading (analog value)
  - Ambient temperature (°C)
  - Relative humidity (%)
- **Output**: Moisture content percentage (%)
- **Preprocessing**: StandardScaler normalization
- **Model File**: `mlmodels/moisture_model/moisture_content_model.joblib`

### 2. Drying Time Prediction Model
- **Algorithm**: Random Forest Regressor
- **Input Features**:
  - Initial moisture content (%)
  - Target/final moisture content (%)
  - Ambient temperature (°C)
  - Relative humidity (%)
- **Output**: Estimated drying time (hours and minutes)
- **Preprocessing**: StandardScaler normalization
- **Model File**: `mlmodels/drying_time_model/drying_time_model.joblib`

### Model Performance
Both models were trained on empirical data collected from field trials and validated for accuracy in real-world agricultural settings.

---

## Hardware Requirements

### Minimum System Requirements
- **Single Board Computer**: Raspberry Pi 4 (2GB RAM minimum, 4GB recommended)
- **Operating System**: Raspbian OS / Ubuntu 20.04+ or Windows 10/11
- **Storage**: 8GB microSD card (16GB+ recommended)
- **Power Supply**: 5V/3A USB-C adapter
- **Connectivity**: USB 2.0 port for Arduino connection

### Sensor Hardware
- **Temperature/Humidity Sensor**: DHT22 (AM2302)
  - Operating Range: -40 to 80°C, 0-100% RH
  - Accuracy: ±0.5°C, ±2% RH
  - Interface: Single-wire digital
  
- **Moisture Sensor**: Capacitive Soil Moisture Sensor
  - Operating Voltage: 3.3-5V DC
  - Output: Analog (0-1023 ADC value)
  - Calibration: `sen_min=246`, `sen_max=570`

- **Microcontroller**: Arduino Uno / ESP32
  - Digital Pin: GPIO 8 (DHT22)
  - Analog Pin: A0 (Moisture Sensor)
  - Communication: USB Serial (115200 baud)

### Circuit Connections
```
Arduino Uno Pinout:
├─ DHT22 Signal    → Pin 8
├─ Moisture Sensor → Pin A0
├─ +5V Supply      → VCC pins
└─ GND             → Common ground

ESP32 Alternative:
├─ DHT22 Signal    → GPIO 8
├─ Moisture Sensor → GPIO 36 (ADC1_CH0)
└─ USB Serial @ 115200
```

---

## Installation

### 1. Hardware Setup
```bash
# Flash Arduino firmware
1. Open Arduino IDE
2. Load: arduino/sensor_reader/sensor_reader.ino
3. Select Board: "Arduino Uno" or "ESP32 Dev Module"
4. Select Port: COM3 (Windows) or /dev/ttyACM0 (Linux)
5. Click Upload
```

### 2. Software Installation (Raspberry Pi / Linux)
```bash
# Clone repository
git clone https://github.com/JenniferTongco/paddy_rice_monitoring_system.git
cd paddy_rice_monitoring_system/website_local

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python main.py
# Database will auto-create on first run
```

### 3. Software Installation (Windows)
```powershell
# Clone repository
git clone https://github.com/JenniferTongco/paddy_rice_monitoring_system.git
cd paddy_rice_monitoring_system\website_local

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### 4. Initial Configuration
```python
# Edit website/__init__.py to configure:
- SECRET_KEY: Change to secure random string
- DB_NAME: SQLite database filename
- REMOTE_URL: Cloud sync endpoint (if using cloud features)
```

---

## Usage

### Starting the Application
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\Activate   # Windows

# Run Flask application
python main.py

# Access web interface
# Open browser: http://localhost:5000
```

### Creating User Accounts
1. Navigate to `/sign-up`
2. Enter farmer details and select municipality/barangay
3. Create account credentials
4. Login at `/login`

### Recording Measurements
1. Ensure Arduino is connected and powered
2. Navigate to "Home" or "Prediction" page
3. Click "Read from Sensor" to capture live data
4. Enter batch details (name, weight, target moisture)
5. View moisture content and predicted drying time
6. Click "Save Prediction" to store record

### Viewing Historical Records
- Navigate to `/records` to view all saved predictions
- Filter by date, batch name, or farmer
- Export data for analysis

### Syncing to Cloud
- Navigate to `/sync-to-remote`
- Enter admin credentials
- Click "Sync Records" to upload local data to cloud

---

## 📡 API Documentation

### Sensor Communication Protocol
```python
# Serial Command Format (Send to Arduino)
Command: "read\n"

# Response Format (Received from Arduino)
Response: "sensor_value,temperature,humidity\n"
Example: "45.2,28.5,65.3\n"
```

### Cloud API Endpoints
```
POST /login
- Authenticate user and obtain token

GET /api/farmers/{username}
- Retrieve farmer profile data

POST /api/sync
- Bulk upload drying records
- Requires Bearer token authentication

GET /api/municipalities
- Fetch all municipalities

GET /api/barangays
- Fetch all barangays
```

---

## Project Structure

```
paddy_rice_monitoring_system/
├── website_local/                    # Edge node application
│   ├── main.py                      # Application entry point
│   ├── requirements.txt             # Python dependencies
│   ├── arduino/
│   │   └── sensor_reader/
│   │       └── sensor_reader.ino    # Arduino firmware (C++)
│   ├── mlmodels/
│   │   ├── drying_time_model/
│   │   │   ├── drying_time_model.joblib      # Trained model
│   │   │   ├── drying_time_scaler.joblib     # Feature scaler
│   │   │   └── predict_drying_time.py        # Inference script
│   │   └── moisture_model/
│   │       ├── moisture_content_model.joblib # Trained model
│   │       ├── moisture_content_scaler.joblib# Feature scaler
│   │       └── predict_moisture.py           # Inference script
│   ├── website/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── models.py                # SQLAlchemy ORM models
│   │   ├── views.py                 # Route handlers & business logic
│   │   ├── auth.py                  # Authentication routes
│   │   ├── api.py                   # Cloud sync API client
│   │   ├── templates/               # Jinja2 HTML templates
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── prediction.html
│   │   │   ├── records.html
│   │   │   ├── readings.html
│   │   │   ├── login.html
│   │   │   └── sign_up.html
│   │   └── static/                  # CSS, JS, assets
│   │       ├── css/
│   │       ├── js/
│   │       └── assets/
│   └── instance/                    # Instance-specific files
│       └── database.db              # SQLite database (auto-generated)
├── README.md                        # This file
└── LICENSE                          # MIT License

```




