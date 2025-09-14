import random
from datetime import datetime
from db.db_utils import SessionLocal, Sensor, Reading, delete_old_readings

def simulate_readings():
    session = SessionLocal()
    sensors = session.query(Sensor).all()
    for sensor in sensors:
        if sensor.type == "temperature":
            value = round(random.uniform(20, 30), 2)
        elif sensor.type == "humidity":
            value = round(random.uniform(40, 70), 2)
        elif sensor.type == "light":
            value = round(random.uniform(100, 800), 2)
        else:
            value = 0

        reading = Reading(sensor_id=sensor.id, value=value, timestamp=datetime.now())
        session.add(reading)

    session.commit()
    session.close()
    delete_old_readings()  # remove old readings
    print("Inserted new readings and cleaned old data")

if __name__ == "__main__":
    simulate_readings()
