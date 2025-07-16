'''
init_db.py
==========
'''

def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS meal_plan (
                id INTEGER PRIMARY KEY,
                day TEXT NOT NULL,
                meal_type TEXT NOT NULL,  -- 'breakfast', 'lunch', or 'dinner'
                meal TEXT NOT NULL
            )
        """)
        conn.commit()