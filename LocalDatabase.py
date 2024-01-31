import sqlite3, os, json

from PySide6.QtCore import QObject

from Constants import SETTINGS_DIR
from RxSignal import RxSignal
from Callsign import Callsign

class LocalDatabase(QObject):
    __TABLES = [
        {'name': 'callsigns',
        'columns': [
            {'name': 'id', 'schema': 'INTEGER PRIMARY KEY'},
            {'name': 'callsign', 'schema': 'TEXT'},
            {'name': 'name', 'schema': 'TEXT'},
            {'name': 'lat', 'schema': 'TEXT'},
            {'name': 'lng', 'schema': 'TEXT'}
        ]},
        {'name' : 'rx_signal',
        'columns': [
            {'name': 'id', 'schema': 'INTEGER PRIMARY KEY'},
            {'name': 'tx', 'schema': 'TEXT'},
            {'name': 'rx', 'schema': 'TEXT'},
            {'name': 'ss', 'schema': 'TEXT'},
            {'name': 'date', 'schema': 'TEXT'}
        ]}
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        db_path = os.path.join(SETTINGS_DIR, "iegmrs.db")
        self.connection = sqlite3.connect(db_path)

    def setup(self):
        cursor = self.connection.cursor()
        rows = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;").fetchall()

        sql_tables = []
        for table in rows:
            sql_tables.append(table[0])

        for table in self.__TABLES:
            if table['name'] not in sql_tables:
                columns = ""
                for idx, col in enumerate(table['columns']):
                    if idx > 0:
                        columns += ", "
                    columns += f"{col['name']} {col['schema']}"

                query = f"CREATE TABLE {table['name']} ({columns})"
                cursor.execute(query)

    def validate(self):
        cursor = self.connection.cursor()
        for table in self.__TABLES:
            query = f"PRAGMA table_info({table['name']});"
            columns = cursor.execute(query).fetchall()
            table_failed = False
            for idx, col in enumerate(columns):
                if col[1] != table['columns'][idx]['name']: table_failed = True

            if table_failed:
                cursor.execute(f"DROP TABLE {table['name']};").fetchall()
                columns = ""
                for idx, col in enumerate(table['columns']):
                    if idx > 0:
                        columns += ", "
                    columns += f"{col['name']} {col['schema']}"

                query = f"CREATE TABLE {table['name']} ({columns})"
                cursor.execute(query)

    def syncSignalData(self, signal_list):
        if signal_list != None:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM rx_signal;")
            for v in signal_list:
                signal = RxSignal(v)
                cursor.execute("INSERT INTO rx_signal (id, tx, rx, ss, date) " 
                               + f"VALUES ('{signal.id}', '{signal.tx}', '{signal.rx}', '{signal.ss}', '{signal.date}')")
            cursor.close()
            self.connection.commit()

    def syncCallsignData(self, signal_list):
        if signal_list != None:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM callsigns;")
            for v in signal_list:
                callsign = Callsign(v)
                cursor.execute("INSERT INTO callsigns (id, callsign, name, lat, lng) " 
                               + f"VALUES ('{callsign.id}', '{callsign.callsign}', '{callsign.name}', '{callsign.lat}', '{callsign.lng}')")
            cursor.close()
            self.connection.commit()

    def fetchRxSignal(self, callsign):
        cursor = self.connection.cursor()
        rows = cursor.execute(f"SELECT rx_signal.*, lat, lng FROM rx_signal LEFT JOIN callsigns ON (callsigns.callsign = tx) WHERE rx LIKE '{callsign}%';").fetchall()
        signals = self.parseSignals(cursor, rows)
        return signals
    
    def fetchTxSignal(self, callsign):
        cursor = self.connection.cursor()
        rows = cursor.execute(f"SELECT rx_signal.*, lat, lng FROM rx_signal LEFT JOIN callsigns ON (callsigns.callsign = rx) WHERE tx LIKE '{callsign}%';").fetchall()
        signals = self.parseSignals(cursor, rows)
        return signals
    
    def fetchCallsigns(self):
        cursor = self.connection.cursor()
        rows = cursor.execute(f"SELECT * FROM callsigns;").fetchall()
        signals = self.parseCallsigns(cursor, rows)
        
        return signals
    
    def parseSignals(self, cursor, rows):
        names = list(map(lambda x: x[0], cursor.description))
        signals = []
        for r in rows:
            v = {}
            for idx, col in enumerate(names):
                v[col] = r[idx]
            signal = RxSignal(v)
            signals.append(signal)
        return signals
    
    def parseCallsigns(self, cursor, rows):
        names = list(map(lambda x: x[0], cursor.description))
        callsigns = []
        for r in rows:
            v = {}
            for idx, col in enumerate(names):
                v[col] = r[idx]
            callsign = Callsign(v)
            callsign.rx_list = self.fetchTxSignal(callsign.callsign)
            callsigns.append(callsign)
        return callsigns