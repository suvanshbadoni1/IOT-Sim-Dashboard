from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Sensor, Reading

# Old (wrong) DB
# DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/iot_sim"

# Correct DB
DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/iotdb"


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# Initialize DB
def init_db():
    Base.metadata.create_all(engine)

# Fetch latest reading per sensor
def get_latest_readings():
    session = SessionLocal()
    sensors = session.query(Sensor).all()
    latest = {}
    for s in sensors:
        r = session.query(Reading).filter(Reading.sensor_id==s.id).order_by(Reading.timestamp.desc()).first()
        if r:
            # Format with proper units and symbols
            if s.type == "temperature":
                latest[s.name] = f"{r.value:.2f} °C"
            elif s.type == "humidity":
                latest[s.name] = f"{r.value:.2f} %"
            elif s.type == "light":
                latest[s.name] = f"{r.value:.2f} lx"
        else:
            latest[s.name] = "No data"
    session.close()
    return latest

# Delete old readings older than 1 hour
def delete_old_readings():
    from datetime import datetime, timedelta
    session = SessionLocal()
    cutoff = datetime.now() - timedelta(hours=1)
    deleted = session.query(Reading).filter(Reading.timestamp < cutoff).delete()
    session.commit()
    session.close()
    print(f"Deleted {deleted} old readings")
