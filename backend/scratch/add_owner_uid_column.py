from app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    print("1. Adding 'owner_uid' column to core.owners table if missing...")
    db.execute(text("ALTER TABLE core.owners ADD COLUMN IF NOT EXISTS owner_uid VARCHAR;"))
    db.commit()
    print("Column added successfully.")

    print("2. Populating owner_uid for existing owners without UID...")
    owners = db.execute(text("SELECT id FROM core.owners WHERE owner_uid IS NULL")).fetchall()
    for row in owners:
        owner_id = row[0]
        uid = f"OWN-{owner_id:06d}"
        db.execute(text("UPDATE core.owners SET owner_uid = :uid WHERE id = :id"), {"uid": uid, "id": owner_id})
    db.commit()
    print(f"Updated {len(owners)} existing owner records with UIDs.")

    print("3. Verifying columns in core.owners table:")
    cols = db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'core' AND table_name = 'owners'")).fetchall()
    print("Columns:", [c[0] for c in cols])

finally:
    db.close()
