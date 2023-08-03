import sqlite3
import time

class ClassDataBase():
    def __init__(self):
        conn = sqlite3.connect("database/user_stats.db")
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            model_output TEXT NOT NULL,
            execution_time REAL NOT NULL
        )
    """)
        conn.commit()
        conn.close()

    def return_data_from_db(self,username:str):
        conn = sqlite3.connect("database/user_stats.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, model_output, execution_time
            FROM user_stats
            WHERE username=?
        """, (username,))

        result = cursor.fetchall()
        conn.close()
        return result


    def save_model_output_to_db(self,username:str, model_output:str, execution_time:str):
                conn = sqlite3.connect("database/user_stats.db")
                cursor = conn.cursor()
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("""
                    INSERT INTO user_stats (username, timestamp, model_output, execution_time)
                    VALUES (?, ?, ?, ?)
                """, (username, timestamp, model_output, execution_time))

                conn.commit()
                conn.close()
