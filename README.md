# Hackerbot Web

Hackerbot web is a web-based interface designed for visualizing maps and interacting with the Hackerbot system. It includes a Flask-based backend and a Vite-powered frontend dashboard.

## Prerequisites
Create and activate a Python virtual environment:

```bash
# Create a virtual environment (venv)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

Additionally, ensure you have `hackerbot_helper` installed by following the instructions in the [Hackerbot WS Repository](https://github.com/AllenChienXXX/hackerbot_ws).

---

## Installation and Setup

### 1. Clone the Repository
Use SSH to clone the repository:
```bash
git clone git@github.com:AllenChienXXX/map_UI.git
```
This will create a directory named `map_UI` and download all necessary files.

### 2. Navigate to the Project Directory
```bash
cd map_UI/
```

## Frontend Setup (`hackerbot-dashboard`)
The frontend is built with Vite and requires Node.js and npm.

### 1. Install Dependencies
```bash
cd hackerbot-dashboard/
npm install
```
> **Note:** If you see warnings related to Node.js versions, ensure you have Node.js 20 or later installed.

### 2. Run the Development Server
```bash
npm run dev -- --host
```
This will start the frontend server. By default, it runs at:
```
http://localhost:5173/
```

## Backend Setup (`flask_app`)
The backend is a Flask-based API.

### 1. Install Dependencies
Navigate to the Flask application directory:
```bash
cd ../flask_app/
```
Install required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Run the Backend Server
```bash
flask run --host=0.0.0.0
```
The backend will run at:
```
http://127.0.0.1:5000
```
