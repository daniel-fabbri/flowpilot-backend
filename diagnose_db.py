"""
Database diagnostic script
"""
import pyodbc
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

DB_SERVER = os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS')
DB_NAME = os.getenv('DB_NAME', 'FlowPilot')
DB_TRUST_CERT = os.getenv('DB_TRUST_CERT', 'yes')

conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={DB_SERVER};'
    f'DATABASE={DB_NAME};'
    f'Trusted_Connection=yes;'
    f'TrustServerCertificate={DB_TRUST_CERT};'
)

print(f"Connecting to: {DB_SERVER}")
print(f"Database: {DB_NAME}\n")

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Check sys.tables
    print("=" * 60)
    print("Checking sys.tables:")
    cursor.execute("SELECT name, schema_id FROM sys.tables ORDER BY name")
    tables = cursor.fetchall()
    print(f"Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]} (schema_id: {table[1]})")
    
    # Check INFORMATION_SCHEMA.TABLES
    print("\n" + "=" * 60)
    print("Checking INFORMATION_SCHEMA.TABLES:")
    cursor.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """)
    info_tables = cursor.fetchall()
    print(f"Found {len(info_tables)} objects:")
    for table in info_tables:
        print(f"  - {table[0]}.{table[1]} ({table[2]})")
    
    # Check all databases
    print("\n" + "=" * 60)
    print("All databases on server:")
    cursor.execute("SELECT name FROM sys.databases ORDER BY name")
    dbs = cursor.fetchall()
    for db in dbs:
        print(f"  - {db[0]}")
    
    # Check current database
    print("\n" + "=" * 60)
    cursor.execute("SELECT DB_NAME()")
    current_db = cursor.fetchone()[0]
    print(f"Current database: {current_db}")
    
    # Check user permissions
    print("\n" + "=" * 60)
    print("Current user:")
    cursor.execute("SELECT SYSTEM_USER, USER_NAME()")
    user_info = cursor.fetchone()
    print(f"System User: {user_info[0]}")
    print(f"Database User: {user_info[1]}")
    
    conn.close()
    print("\n✅ Diagnostic completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
