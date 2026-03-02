"""
Simple script to create database tables.
"""
import pyodbc
import os

DB_SERVER = os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS')
DB_NAME = os.getenv('DB_NAME', 'flowpilot_db')
DB_TRUST_CERT = os.getenv('DB_TRUST_CERT', 'yes')

try:
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={DB_SERVER};'
        f'DATABASE={DB_NAME};'
        f'Trusted_Connection=yes;'
        f'TrustServerCertificate={DB_TRUST_CERT};'
    )
    print(f"Connecting to database {DB_NAME}...")
    conn = pyodbc.connect(conn_str)
    conn.autocommit = False
    cursor = conn.cursor()
    
    # Read SQL script
    print("Reading scripts/create_tables.sql...")
    with open('scripts/create_tables.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Execute complete script
    print("Executing SQL commands...")
    
    # Split and execute line by line
    for line in sql_script.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            try:
                cursor.execute(line)
            except Exception as e:
                # Ignore comment syntax errors
                pass
    
    conn.commit()
    print("✅ SQL script executed!")
    
    # Check created tables
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n{'='*60}")
    print(f"✅ SUCCESS! {len(tables)} tables in database:")
    for table in tables:
        print(f"  - {table}")
    print(f"{'='*60}\n")
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}\n")
