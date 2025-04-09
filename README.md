

✅ Recommended Setup for Flask on Raspberry Pi
1. Use gunicorn as your WSGI server
Install it inside your virtual environment (or globally if preferred):
pip install gunicorn
Run your app with:
gunicorn -w 2 -b 0.0.0.0:8000 'website:create_app()'
    -w 2 = 2 worker processes (enough for a Pi)
    -b = bind to host:port

2. (Optional) Use systemd to run Flask as a service
So it starts automatically on boot and runs in the background.
Create a service file:
sudo nano /etc/systemd/system/riceapp.service
Paste this (adjust paths as needed):
[Unit]
Description=Flask Rice Drying App
After=network.target
[Service]
User=pi
WorkingDirectory=/home/pi/your_project_directory
ExecStart=/home/pi/your_project_directory/venv/bin/gunicorn -w 2 -b 0.0.0.0:8000 'website:create_app()'
Restart=always
[Install]
WantedBy=multi-user.target
Then enable and start the service:
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable riceapp
sudo systemctl start riceapp
Check its status:
sudo systemctl status riceapp

3. (Optional) Reverse proxy with Nginx
If you want it to run on port 80 (so you can go to http://raspberrypi.local/), you can install Nginx and forward requests to gunicorn.

4. Make sure it's safe
    • Don't run with debug=True.
    • Use proper error handling in Flask.
    • Don’t expose unnecessary ports to the internet.

Let me know:
    • Do you want to make it auto-start on boot?
    • Do you want it accessible locally only or on your LAN?
    • Do you need help setting up Nginx reverse proxy?
I can walk you through any of these!


Perfect — here's how to set up your Raspberry Pi Flask app to:
    1. ✅ Auto-start on boot
    2. ✅ Run locally (accessible via LAN)
    3. ✅ Sync/update a remote database only when internet is available

✅ Step 1: Auto-Start Flask App on Boot
We'll use systemd to create a service.
🔧 Create a systemd service
sudo nano /etc/systemd/system/riceapp.service
Paste this content:
Replace paths and names as needed.
[Unit]
Description=Flask Rice Drying App
After=network.target
[Service]
User=pi
WorkingDirectory=/home/pi/your_project_directory
ExecStart=/home/pi/your_project_directory/venv/bin/gunicorn -w 2 -b 0.0.0.0:8000 'website:create_app()'
Restart=always
[Install]
WantedBy=multi-user.target
Enable & start it:
sudo systemctl daemon-reload
sudo systemctl enable riceapp
sudo systemctl start riceapp
Your app now runs automatically after boot.

✅ Step 2: Run Locally (LAN access)
You’re already binding to 0.0.0.0:8000, so any device on the same Wi-Fi network can access it via:
http://<raspberrypi_ip>:8000
Find your Pi’s IP:
hostname -I

✅ Step 3: Sync to Online Server if Internet is Present
This logic will be handled in Python, possibly using requests to hit your live server's API.
Example Sync Code
import requests
import socket
def is_internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False
def sync_record_to_server(data):
    if is_internet_available():
        try:
            response = requests.post("https://your-live-server.com/api/sync", json=data)
            if response.status_code == 200:
                print("Synced successfully!")
        except Exception as e:
            print("Sync failed:", e)
You can run this after saving a record locally — no internet? Skip syncing.

Optional Enhancements
    • 📁 Use SQLite locally, and sync only new entries.
    • 🕓 Use a background job or scheduled task (e.g., cron or apscheduler) to sync periodically.
    • 🛡️ Make sure the API is secure (auth, validation, etc.).

