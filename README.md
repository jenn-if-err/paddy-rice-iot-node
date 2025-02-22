# paddy_rice_monitoring_system

paddy-drying-prediction/
├── README.md                # Project overview and repository structure details.
├── LICENSE                  # Project license (e.g., MIT License).
├── .gitignore               # Files and directories to be excluded from version control.
├── arduino/                 # Arduino code for sensor data acquisition.
│   ├── sensor_reader.ino    # Sketch to read data from DHT and moisture sensors.
│   └── README.md            # Instructions on wiring, setup, and flashing the Arduino.
├── models/                  # Machine learning models and training scripts.
│   ├── moisture_model/      
│   │   ├── train.py         # Script to train/fine-tune the MLP model for moisture estimation.
│   │   ├── model.h5         # Pre-trained moisture model.
│   │   └── README.md        # Documentation and usage for the moisture model.
│   ├── drying_time_model/   
│   │   ├── train.py         # Script to train/fine-tune the MLP model for drying time prediction.
│   │   ├── model.h5         # Pre-trained drying time model.
│   │   └── README.md        # Documentation and usage for the drying time model.
│   └── utils.py             # Shared utility functions for preprocessing and model handling.
├── data/                    # Data files for training and inference.
│   ├── raw/                 # Raw sensor data files.
│   └── processed/           # Processed data files ready for model consumption.
├── scripts/                 # Python scripts to tie the workflow together.
│   ├── data_acquisition.py  # Reads sensor data from the Arduino (via serial connection).
│   ├── predict.py           # Uses sensor data to predict moisture and drying time, then computes shelf life and yield.
│   └── pipeline.py          # Orchestrates the continuous process of data acquisition and prediction.
├── website/                 # Web application to display prediction results.
│   ├── app.py               # Web server (e.g., using Flask or Django) that serves the web app.
│   ├── templates/           # HTML templates for the web interface.
│   ├── static/              # Static assets such as CSS, JavaScript, and images.
│   └── README.md            # Instructions on running and configuring the web app.
└── requirements.txt         # Python dependencies for the project.
