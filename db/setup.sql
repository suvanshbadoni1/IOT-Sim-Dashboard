-- Connect to the database
\c iotdb;

-- Table to store sensor info
CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    unit VARCHAR(10) NOT NULL
);

-- Insert default sensors
INSERT INTO sensors (name, type, unit) VALUES
('Temperature', 'temperature', '°C'),
('Humidity', 'humidity', '%'),
('Light', 'light', 'lx');

-- Table to store sensor readings
CREATE TABLE IF NOT EXISTS readings (
    id SERIAL PRIMARY KEY,
    sensor_id INT REFERENCES sensors(id) ON DELETE CASCADE,
    value FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
