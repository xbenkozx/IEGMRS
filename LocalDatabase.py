import sqlite3, os, json

from PySide6.QtCore import QObject

from Constants import SETTINGS_DIR

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

    def syncLocalVehicles(self, signal_list):
        if signal_list != None:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM vehicles;")
            for v in signal_list:
                vehicle = RxSignal(v)
                vehicle.parse(v)
                cursor.execute("INSERT INTO vehicles (id, stock, vin, make, model, series, color, year, status, status_code, keys_quantity, keybox_id, keybox_serial, is_checked_out, check_out_user, keybox_id_2, keybox_serial_2, is_checked_out_2, check_out_user_2, last_update_key_1, last_update_key_2) " 
                               + f"VALUES ('{vehicle.id}', '{vehicle.stock}', '{vehicle.vin}', '{vehicle.make}', '{vehicle.model}', '{vehicle.series}', '{vehicle.color}', '{vehicle.year}', '{vehicle.status}', '{vehicle.status_code}', '{vehicle.keys_quantity}', '{vehicle.keybox_id}', '{vehicle.keybox_serial}', '{vehicle.is_checked_out}', '{vehicle.check_out_user}', '{vehicle.keybox_id_2}', '{vehicle.keybox_serial_2}', '{vehicle.is_checked_out_2}', '{vehicle.check_out_user_2}', '{vehicle.last_update_key_1}', '{vehicle.last_update_key_2}')")
            cursor.close()
            self.connection.commit()