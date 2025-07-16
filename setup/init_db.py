"""Initialisation des tables"""

from shared_data.database import engine
from shared_data.models import Base
import time
import socket

def wait_for_db(host: str, port: int, timeout=30):
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("✅ Database is ready.")
                return
        except OSError:
            if time.time() - start > timeout:
                raise TimeoutError(f"⏰ Database not ready after {timeout} seconds")
            print("⏳ Waiting for database...")
            time.sleep(1)

wait_for_db("db", 5432)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")
