import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://user:pass@db:5432/testdb"

engine = create_engine(DATABASE_URL)

for i in range(10):
    try:

        conn = engine.connect()
        conn.close()
        print("DB connected")
        break
    except Exception:
        print("DB not ready, retrying...")
        time.sleep(2)
else:
    raise Exception("DB connection failed")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
