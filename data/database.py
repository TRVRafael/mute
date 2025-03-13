import sqlite3

from data.config import db_logger

class Database:
    def __init__(self, database_name = "data/database.db"):
        self._conn = sqlite3.connect(database_name, check_same_thread=False)
        self._cursor = self._conn.cursor()
        self._init_muted_expressions_table()
        self._init_record_muted_expressions_table()
        
    def _init_muted_expressions_table(self):
        try:
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS muted_expressions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    responsable TEXT,
                    expression TEXT,
                    timestamp TEXT
                )
            """)
            self._conn.commit()
            db_logger.info("Created initial Muted Expression table.")
        except Exception as err:
            db_logger.error(f"Error creating initial Muted Expression table ->\n{err}")
            
    def _init_record_muted_expressions_table(self):
        try:
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS expression_record (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    responsable TEXT,
                    expression TEXT,
                    timestamp TEXT
                )
            """)
            self._conn.commit()
            db_logger.info("Created initial Expression Record table.")
        except Exception as err:
            db_logger.error(f"Error creating initial Expression Record table ->\n{err}")
            
    def _init_expression_table(self, expression: str):
        try:
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {expression} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    message TEXT,
                    timestamp TEXT
                )
            """)
            self._conn.commit()
            db_logger.info(f"Created {expression} table.")
        except Exception as err:
            db_logger.error(f"Error creating {expression} table ->\n{err}")
    
    def insert_muted_expression(self, responsable: str, expression: str, timestamp: str):
        try:
            self._cursor.execute(f"INSERT OR IGNORE INTO muted_expressions (responsable, expression, timestamp) VALUES (?, ?, ?);", (responsable, expression, timestamp))
            self._conn.commit()
            db_logger.info(f"Inserted {expression} in Muted Expressions table")
            self._init_expression_table(expression)
        except Exception as err:
            db_logger.error(f"Error inserting expression {expression} in Muted Expressions table ->\n{err}")
            
    def insert_affected(self, expression: str, username: str, message: str, timestamp: str):
        try:
            self._cursor.execute(f"INSERT OR IGNORE INTO {expression} (username, message, timestamp) VALUES (?, ?, ?);", (username, message, timestamp))
            self._conn.commit()
            db_logger.info(f"Inserted {username} in {expression} table")
            self._init_expression_table(expression)
        except Exception as err:
            db_logger.error(f"Error inserting {username} in {expression} table ->\n{err}")
            
    def _insert_expression_record(self, responsable, expression, timestamp):
        try:
            self._cursor.execute(f"INSERT OR IGNORE INTO expression_record (responsable, expression, timestamp) VALUES (?, ?, ?);", (responsable, expression, timestamp))
            self._conn.commit()
            db_logger.info(f"Inserted {expression} in Expression Record table")
        except Exception as err:
            db_logger.error(f"Error inserting expression {expression} in Expression Record table ->\n{err}")
        
    def remove_muted_expression(self, responsable: str, expression: str, timestamp: str):
        try:
            self._cursor.execute(f"DELETE FROM muted_expressions WHERE expression=?;", (expression,))
            self._conn.commit()
            db_logger.info(f"Removed {expression} in Muted Expressions table")
            self._insert_expression_record(responsable, expression, timestamp)
        except Exception as err:
            db_logger.error(f"Error inserting expression {expression} in Muted Expressions table ->\n{err}")

    def get_expression_info(self, expression: str):
        try:
            self._cursor.execute(f"SELECT expression FROM {expression};")
            result = self._cursor.fetchall()
            db_logger.info(f"Got all info about {expression}")
            return result
        except Exception as err:
            db_logger.error(f"Error getting all info about {expression} ->\n{err}")
            return []
            
    def get_muted_expressions(self):
        try:
            self._cursor.execute("SELECT expression FROM muted_expressions;")
            result = self._cursor.fetchall()
            db_logger.info(f"Got all muted expressions")
            return result
        except Exception as err:
            db_logger.error(f"Error getting all muted expressions ->\n{err}")
            return []
        
    def get_affected(self, expression: str):
        try:
            self._cursor.execute(f"SELECT username, message, timestamp FROM {expression};")
            result = self._cursor.fetchall()
            db_logger.info(f"Got all affected by {expression}")
            return result
        except Exception as err:
            db_logger.error(f"Error getting all affected by {expression} ->\n{err}")
            return []
        
    def get_affected_info(self, expression, username):
        try:
            self._cursor.execute(f"SELECT username, message, timestamp FROM {expression} WHERE username=?;", (username,))
            result = self._cursor.fetchall()
            db_logger.info(f"Got all affected by {expression}")
            return result
        except Exception as err:
            db_logger.error(f"Error getting all affected by {expression} ->\n{err}")
            return []
        
    def get_expression_responsable(self, expression):
        try:
            self._cursor.execute(f"SELECT responsable, timestamp FROM muted_expressions WHERE expression=?;", (expression,))
            result = self._cursor.fetchall()
            db_logger.info(f"Got responsable by {expression}")
            return result
        except Exception as err:
            db_logger.error(f"Error getting responsable by {expression} ->\n{err}")
            return []
        
db_controller = Database()