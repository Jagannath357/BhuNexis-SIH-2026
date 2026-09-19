from app.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    rows = conn.execute(text("SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype = 'c'")).fetchall()
    for name, cdef in rows:
        print(f"{name}: {cdef}")
