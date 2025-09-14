# IOT-Sim-Dashboard

## Overview

IoT Simulation Dashboard is a **Python-based web application** that simulates IoT sensor data (Temperature, Humidity, Light), stores it in a **PostgreSQL database**, and displays the latest readings on a **live web dashboard**.

* No IoT hardware required.
* Auto-refresh dashboard with latest readings.
* Shows **current time, date, and location** based on browser.
* Automatically deletes sensor data older than 1 hour.
* Responsive UI using **Bootstrap 5**.

---

## Features

* Simulate sensor readings: Temperature (°C), Humidity (%), Light (lx).
* Store readings in **PostgreSQL** (`iotdb`).
* Fetch **latest readings** from database for live dashboard.
* Auto-delete readings older than 1 hour.
* Show **browser-based location and city name**.
* Display notes explaining units and calculations.

---

## File Structure & Descriptions

```
IoT-Sim-Dashboard/
│
├── db/
│   ├── setup.sql         # SQL script: creates tables and inserts default sensors
│   ├── models.py         # SQLAlchemy models for Sensors and Readings
│   └── db_utils.py       # Functions for DB operations: insert, fetch, delete readings
│
├── simulator.py          # Simulates sensor readings and inserts into DB
├── web/
│   ├── app.py            # Flask app serving dashboard and API
│   ├── templates/
│   │   └── dashboard.html  # HTML dashboard using Bootstrap 5
│   └── static/           # CSS, JS, images (optional)
│
├── requirements.txt      # Python dependencies (Flask, SQLAlchemy, psycopg2, pytz)
└── README.md             # Project documentation (this file)
```

---

## Database Setup (`iotdb`)
DataBase : postgres 17.6-1 Port : 5432 Password : 12345
PG Bouncer Port : 6432
POSTGRES SQL
            -- Create database
        CREATE DATABASE iotdb;

        -- Create user with password
        CREATE USER iotuser WITH PASSWORD 'iotpass';

        -- Grant privileges
        GRANT ALL PRIVILEGES ON DATABASE iotdb TO iotuser;
        
**Database Name:** `iotdb`

### Tables

**1. `sensors`** – stores sensor info

| Column | Type               | Description                                      |
| ------ | ------------------ | ------------------------------------------------ |
| id     | SERIAL PRIMARY KEY | Unique sensor ID                                 |
| name   | VARCHAR(50)        | Sensor name                                      |
| type   | VARCHAR(50)        | Sensor type (`temperature`, `humidity`, `light`) |
| unit   | VARCHAR(10)        | Measurement unit (`°C`, `%`, `lx`)               |

**Default data:**

```sql
INSERT INTO sensors (name, type, unit) VALUES
('Temperature', 'temperature', '°C'),
('Humidity', 'humidity', '%'),
('Light', 'light', 'lx');
```

**2. `readings`** – stores simulated sensor readings

| Column     | Type                                 | Description       |
| ---------- | ------------------------------------ | ----------------- |
| id         | SERIAL PRIMARY KEY                   | Unique reading ID |
| sensor\_id | INT REFERENCES sensors(id)           | Sensor reference  |
| value      | FLOAT                                | Reading value     |
| timestamp  | TIMESTAMP DEFAULT CURRENT\_TIMESTAMP | Reading time      |

**Auto-cleanup:**

```sql
DELETE FROM readings WHERE timestamp < NOW() - INTERVAL '1 hour';
```

---

## Simulator (`simulator.py`)

* Generates **random values** for each sensor:

  * Temperature: 20–30 °C
  * Humidity: 40–70 %
  * Light: 100–800 lx
* Inserts readings into `readings` table with timestamp.
* Deletes readings older than **1 hour** automatically.

---

## Dashboard (`web/app.py`)

* `/` → renders **dashboard.html**
* `/api/readings` → returns latest readings in JSON
* Fetches readings from **PostgreSQL database** using SQLAlchemy
* Displays:

| Sensor      | Latest Value |
| ----------- | ------------ |
| Temperature | 22.68 °C     |
| Humidity    | 49.11 %      |
| Light       | 173.21 lx    |

* Shows **current time, date, and browser-based location**.
* Uses **Bootstrap 5** for responsive table and UI.

---

## How Data Flows

1. `simulator.py` → generates readings → inserts into `iotdb.readings`.
2. Flask `/api/readings` → fetches latest reading per sensor from DB.
3. Dashboard → renders **Bootstrap table** with live values.
4. **Cleanup** → old readings deleted after 1 hour automatically.

---

## Dependencies

```bash
Flask==2.3.0
SQLAlchemy==2.0.20
psycopg2-binary==2.9.9
pytz==2025.7
```

Install via:

```bash
pip install -r requirements.txt
```

---

## Running the Project

1. **Create database**:

```bash
psql -U postgres -h localhost -p 5432
CREATE DATABASE iotdb;
\c iotdb
-- Run setup.sql
\i path/to/db/setup.sql
```

2. **Run simulator**:

```bash
python simulator.py
```

3. **Run Flask app**:

```bash
cd web
python app.py
```

4. Open browser:

```
http://127.0.0.1:5000/
```

---

## Notes

* **°C** = Temperature in degrees Celsius
* **%** = Relative Humidity
* **lx** = Light intensity in lux
* Location is fetched using **browser geolocation** and reverse geocoding for city name

---

## Optional Enhancements

* Color-coded readings (hot/cold, bright/dim)
* Graphs for historical data
* Automated scheduling using cron or APScheduler

