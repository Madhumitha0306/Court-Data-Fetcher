import sqlite3

def init_db():
    conn = sqlite3.connect('court_logs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            filing_year TEXT,
            raw_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_log(case_type, case_number, filing_year, raw_response):
    conn = sqlite3.connect('court_logs.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO logs (case_type, case_number, filing_year, raw_response)
        VALUES (?, ?, ?, ?)
    ''', (case_type, case_number, filing_year, raw_response))
    conn.commit()
    conn.close()

