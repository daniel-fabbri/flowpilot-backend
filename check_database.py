"""
Script to check database connection and create tables if needed.
"""
import pyodbc
import os

# Database configuration
DB_SERVER = os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS')
DB_NAME = os.getenv('DB_NAME', 'flowpilot_db')
DB_TRUST_CERT = os.getenv('DB_TRUST_CERT', 'yes')

def check_database_exists():
    """Check if database exists"""
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE=master;'
            f'Trusted_Connection=yes;'
            f'TrustServerCertificate={DB_TRUST_CERT};'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{DB_NAME}'")
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def create_database():
    """Create the database"""
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE=master;'
            f'Trusted_Connection=yes;'
            f'TrustServerCertificate={DB_TRUST_CERT};'
        )
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print(f"Creating database {DB_NAME}...")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"✅ Database {DB_NAME} created successfully!")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create database tables"""
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'Trusted_Connection=yes;'
            f'TrustServerCertificate={DB_TRUST_CERT};'
        )
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read SQL script
        with open('scripts/create_tables.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Execute each SQL command separately
        commands = sql_script.split(';')
        
        print("Creating tables...")
        for command in commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    conn.commit()
                except Exception as e:
                    if "already an object" not in str(e):
                        print(f"⚠️  Warning: {e}")
        
        print("✅ Tables created successfully!")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def check_connection():
    """Test database connection"""
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'Trusted_Connection=yes;'
            f'TrustServerCertificate={DB_TRUST_CERT};'
        )
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Check existing tables
        cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        tables = [f"{row[0]}.{row[1]}" for row in cursor.fetchall()]
        
        print("\n" + "="*60)
        print(f"✅ Connection established successfully!")
        print(f"Server: {DB_SERVER}")
        print(f"Database: {DB_NAME}")
        print(f"\nTables found ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")
        print("="*60 + "\n")
        
        conn.close()
        return True
    except Exception as e:
        print(f"\n❌ Connection error: {e}\n")
        return False

def main():
    print("🔍 Checking SQL Server database...")
    print(f"Server: {DB_SERVER}")
    print(f"Database: {DB_NAME}\n")
    
    # 1. Check if database exists
    if not check_database_exists():
        print(f"⚠️  Database {DB_NAME} not found.")
        print("📝 Creating database automatically...")
        if not create_database():
            return
    else:
        print(f"✅ Database {DB_NAME} found!")
    
    # 2. Try to connect and check tables
    if not check_connection():
        print("⚠️  Could not connect to database.")
        print("📝 Creating tables automatically...")
        create_tables()
        check_connection()
    
    print("\n📝 Current .env configuration:")
    print(f"DB_SERVER={DB_SERVER}")
    print(f"DB_NAME={DB_NAME}")
    print(f"DB_TRUST_CERT={DB_TRUST_CERT}")
    print("\n✅ Check completed!")

if __name__ == "__main__":
    main()
