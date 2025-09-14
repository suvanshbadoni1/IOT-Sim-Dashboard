from db.models import Base
from db.db_utils import engine, insert_sensor, load_config

def init_database():
    # Create tables
    Base.metadata.create_all(engine)

    # Load sensors from config
    cfg = load_config()
    for s in cfg["sensors"]:
        insert_sensor(s["name"], s["type"], s["unit"])

if __name__ == "__main__":
    init_database()
    print("✅ PostgreSQL database initialized with sensors")
