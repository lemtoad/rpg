import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, db_path: str = 'chat_history.db') -> None:
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.c = self.conn.cursor()
            self.logger = logger
            self.initialize_database()
        except sqlite3.DatabaseError as e:
            self.logger.exception("Database connection error")

    def initialize_database(self):
        try:
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    discord_id TEXT PRIMARY KEY,
                    level INTEGER,
                    exp INTEGER,
                    gold INTEGER,
                    current_health INTEGER,
                    max_health INTEGER,
                    attack INTEGER,
                    defense INTEGER,
                    inventory TEXT,
                    equipment TEXT,
                    base_attack INTEGER DEFAULT 10,
                    base_defense INTEGER DEFAULT 5,
                    stat_points INTEGER DEFAULT 0,
                    active_quest INTEGER DEFAULT 0,
                    lymian_empire_state TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            self.logger.exception("Failed to initialize database")

    def execute(self, query: str, params: tuple = ()):
        try:
            self.c.execute(query, params)
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            self.logger.exception("Failed to execute query")

    def fetchone(self, query: str, params: tuple = ()):
        try:
            self.c.execute(query, params)
            result = self.c.fetchone()
            return result
        except sqlite3.DatabaseError as e:
            self.logger.exception("Failed to fetchone")
            return None

    def fetchall(self, query: str, params: tuple = ()):
        try:
            self.c.execute(query, params)
            results = self.c.fetchall()
            return results
        except sqlite3.DatabaseError as e:
            self.logger.exception("Failed to fetchall")
            return []

    def row_count(self):
        return self.c.rowcount

    def close(self):
        try:
            self.conn.close()
        except sqlite3.DatabaseError as e:
            self.logger.exception("Failed to close database connection")
