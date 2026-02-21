import sqlite3

def setup_impact_database():
    print("Bulding the Program Impact Database (SQLite)...")

    conn = sqlite3.connect("program_impact.db")
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS program_pitch")

    cursor.execute("""
        CREATE TABLE program_pitch (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_name, TEXT,
            target_tier TEXT,
            total_budget_usd REAL,
            projected_student_reach INTEGER,
            projected_social_value_usd REAL
            )
        """)
    proposal_data = [
        (
            'Elephant and Piggie Emotional Literacy Rollout',
            'Tier 2',
            45000.00,
            3000,
            81000.00
        )
    ]

    cursor.executemany("""
        INSERT INTO program_pitch
        (program_name, target_tier, total_budget_usd, projected_student_reach, projected_social_value_usd)
        VALUES (?, ?, ?, ?, ?)
    """, proposal_data)

    conn.commit()
    conn.close()

    print("Database successfully created: 'program_impact.db'")
    print("Table 'program_pitch' populated with Elephant and Piggie metrics.")

if __name__ == "__main__":
    setup_impact_database()
