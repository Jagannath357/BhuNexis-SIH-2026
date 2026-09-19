from app.db.session import SessionLocal
from sqlalchemy import text
from app.models.all_models import Base, User, Document, Owner, Parcel, LandRight, DocumentPage, ExtractedField, ValidationResult, ReviewCase, AuditEvent

db = SessionLocal()

models = [User, Document, Owner, Parcel, LandRight, DocumentPage, ExtractedField, ValidationResult, ReviewCase, AuditEvent]

print("Comparing SQLAlchemy Models vs Database Tables:")
for model in models:
    table_name = model.__tablename__
    schema = getattr(model, "__table_args__", {}).get("schema", "public") if isinstance(getattr(model, "__table_args__", {}), dict) else "core"
    
    # DB columns
    res = db.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{table_name}'")).fetchall()
    db_cols = set(r[0] for r in res)
    
    # Model columns
    model_cols = set(c.name for c in model.__table__.columns)
    
    missing_in_db = model_cols - db_cols
    
    if missing_in_db:
        print(f"MISSING IN DB -> Table '{schema}.{table_name}': {missing_in_db}")
    else:
        print(f"OK -> Table '{schema}.{table_name}' matches DB columns.")
