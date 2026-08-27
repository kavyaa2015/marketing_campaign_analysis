import sqlite3
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "marketing_campaign.db"
SQL_PATH = BASE_DIR / "sql" / "analytical_queries.sql"


# ============================================================
# RUN SQL
# ============================================================

print("=" * 60)
print("RUNNING MARKETING ANALYTICAL SQL")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_script = file.read()

conn.executescript(sql_script)

conn.commit()

print("\nSQL script executed successfully.")

# ============================================================
# TEST VIEWS
# ============================================================

cursor = conn.cursor()

print("\nOverall KPI:")
cursor.execute("SELECT * FROM vw_overall_kpis;")
print(cursor.fetchall())

print("\nCampaign Performance:")
cursor.execute("SELECT * FROM vw_campaign_performance;")

for row in cursor.fetchall():
    print(row)

print("\nCountry Analysis:")
cursor.execute("SELECT * FROM vw_country_analysis;")

for row in cursor.fetchall():
    print(row)

print("\nAge Analysis:")
cursor.execute("SELECT * FROM vw_age_analysis;")

for row in cursor.fetchall():
    print(row)

print("\nSegment Analysis:")
cursor.execute("SELECT * FROM vw_segment_analysis;")

for row in cursor.fetchall():
    print(row)

conn.close()

print("\n" + "=" * 60)
print("SQL ANALYSIS COMPLETED")
print("=" * 60)