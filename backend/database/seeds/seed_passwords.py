import psycopg
import bcrypt

def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

conn = psycopg.connect("postgresql://postgres:postgres@localhost:5432/bhunexis")
cur = conn.cursor()

print("1. Updating role constraint on core.users...")
cur.execute("""
    ALTER TABLE core.users DROP CONSTRAINT IF EXISTS users_role_check;
    ALTER TABLE core.users ADD CONSTRAINT users_role_check 
    CHECK (role::text = ANY (ARRAY['ADMIN', 'OFFICER', 'REVIEWER', 'AUDITOR', 'CITIZEN', 'REVENUE_OFFICER', 'SURVEY_OFFICER']::text[]));
""")
conn.commit()
print("Constraint updated successfully!")

print("2. Seeding passwords for existing users...")
default_hash = hash_pw("password123")

cur.execute("SELECT id, email, role FROM core.users;")
users = cur.fetchall()

for u in users:
    uid, email, role = u[0], u[1], u[2]
    cur.execute("UPDATE core.users SET password_hash = %s WHERE id = %s;", (default_hash, uid))
    print(f"Updated user ID={uid} ({email}) password to 'password123'")

conn.commit()

print("3. Seeding default Citizen user...")
cur.execute("SELECT id FROM core.users WHERE email = 'citizen@bhunexis.demo';")
if not cur.fetchone():
    cur.execute("""
        INSERT INTO core.users (full_name, email, password_hash, role, phone, is_active)
        VALUES ('Ramesh Chandra Das', 'citizen@bhunexis.demo', %s, 'CITIZEN', '9876543210', true);
    """, (default_hash,))
    conn.commit()
    print("Default citizen account 'citizen@bhunexis.demo' created!")
else:
    print("Citizen account already exists.")

conn.close()
print("Seed & Migration complete!")
