import sqlite3
import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "marketing_cleaned.csv"
)

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = DATABASE_DIR / "marketing_campaign.db"

SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


# ============================================================
# LOAD CSV
# ============================================================

print("=" * 60)
print("LOADING MARKETING DATA INTO SQLITE")
print("=" * 60)

df = pd.read_csv(CSV_PATH)

print(f"CSV rows    : {len(df):,}")
print(f"CSV columns : {len(df.columns)}")


# ============================================================
# CONNECT
# ============================================================

connection = sqlite3.connect(DB_PATH)


# ============================================================
# CREATE SCHEMA
# ============================================================

with open(
    SCHEMA_PATH,
    "r",
    encoding="utf-8"
) as file:

    schema_sql = file.read()

connection.executescript(schema_sql)


# ============================================================
# LOAD DATA
# ============================================================

# Keep only columns that exist in the SQL table.
table_columns = [
    row[1]
    for row in connection.execute(
        "PRAGMA table_info(customers)"
    ).fetchall()
]

available_columns = [
    column
    for column in table_columns
    if column in df.columns
]

df_to_load = df[available_columns].copy()


df_to_load.to_sql(
    "customers",
    connection,
    if_exists="append",
    index=False
)


# ============================================================
# VERIFY
# ============================================================

count = connection.execute(
    "SELECT COUNT(*) FROM customers"
).fetchone()[0]

print(f"\nCustomers loaded : {count:,}")


print("\nTables:")

tables = connection.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    """
).fetchall()

for table in tables:
    print(f"  ✓ {table[0]}")


connection.close()


print("\n" + "=" * 60)
print("DATABASE LOADING COMPLETED")
print("=" * 60)

print(f"\nDatabase:")
print(DB_PATH)