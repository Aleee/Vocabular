from PyQt6.QtSql import *
from typing import *
import lovely_logger as log


class DbHandler:
    def __init__(self):
        self.db: QSqlDatabase = QSqlDatabase("QSQLITE")
        self.connected_state: bool = False

    def create_connection(self, path: str) -> bool:
        self.db.setDatabaseName(path)
        self.connected_state = self.db.open()
        if not self.connected_state:
            log.error(f"Could not connect to database with given path \'{path}\'")
        return self.connected_state

    def exec_query(self, query: QSqlQuery) -> bool:
        if not self.connected_state:
            log.error(f"Query \'{query.lastQuery()}\' was not executed as there is no active DB connection")
            return False
        result = query.exec()
        if result:
            return True
        else:
            log.error(f"Query {query.lastQuery()} failed with error: {query.lastError()}")
            return False
