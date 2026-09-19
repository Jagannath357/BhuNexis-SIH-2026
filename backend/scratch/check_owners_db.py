from app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("Checking core.owners columns:")
res = db.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'core' AND table_name = 'owners'")).fetchall()
for col, dt in res:
    print(f"  {col}: {dt}")

print("\nChecking all tables in core schema:")
tables = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'core'")).fetchall()
for t in tables:
    print("  Table:", t[0])
