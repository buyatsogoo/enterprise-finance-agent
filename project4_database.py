import sqlite3

def setup_corporate_database():
    print("🏢 Building the Corporate 'InfoCube' (SQLite Database)...")
    
    # 1. Connect to (or create) the database file
    conn = sqlite3.connect("corporate_finance.db")
    cursor = conn.cursor()

    # 2. Clear out old tables if you run this multiple times
    cursor.execute("DROP TABLE IF EXISTS actuals")
    cursor.execute("DROP TABLE IF EXISTS targets")

    # 3. Create the Actuals table (Historical Data)
    cursor.execute("""
        CREATE TABLE actuals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quarter TEXT,
            account_category TEXT,
            amount REAL
        )
    """)

    # 4. Create the Targets table (Forecasted Data)
    cursor.execute("""
        CREATE TABLE targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quarter TEXT,
            account_category TEXT,
            amount REAL
        )
    """)

    # 5. Insert mock Q1-Q3 Actuals
    historical_data = [
        ('Q1', 'Revenue', 5000000), ('Q1', 'COGS', 2000000), ('Q1', 'OPEX', 1500000),
        ('Q2', 'Revenue', 5200000), ('Q2', 'COGS', 2100000), ('Q2', 'OPEX', 1600000),
        ('Q3', 'Revenue', 5400000), ('Q3', 'COGS', 2200000), ('Q3', 'OPEX', 1700000),
        # Q4 Actuals (Showing a revenue miss and an OPEX spike)
        ('Q4', 'Revenue', 5100000), ('Q4', 'COGS', 2300000), ('Q4', 'OPEX', 2400000)
    ]
    cursor.executemany("INSERT INTO actuals (quarter, account_category, amount) VALUES (?, ?, ?)", historical_data)

    # 6. Insert mock Q4 Targets (What the business EXPECTED to happen)
    forecast_data = [
        ('Q4', 'Revenue', 5800000), 
        ('Q4', 'COGS', 2300000), 
        ('Q4', 'OPEX', 1800000) 
    ]
    cursor.executemany("INSERT INTO targets (quarter, account_category, amount) VALUES (?, ?, ?)", forecast_data)

    # 7. Save and close
    conn.commit()
    conn.close()
    
    print("✅ Database successfully created: 'corporate_finance.db'")
    print("✅ Tables 'actuals' and 'targets' populated with data.")

if __name__ == "__main__":
    setup_corporate_database()