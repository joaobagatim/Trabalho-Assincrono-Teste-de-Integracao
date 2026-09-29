import sqlite3


class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript("""
            CREATE TABLE aeronaves (
                id INTEGER PRIMARY KEY,
                matricula TEXT NOT NULL UNIQUE,
                status_manutencao TEXT NOT NULL
            );
            CREATE TABLE pilotos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL
            );
            CREATE TABLE agendamentos (
                id INTEGER PRIMARY KEY,
                aeronave_id INTEGER NOT NULL REFERENCES aeronaves(id),
                piloto_id INTEGER NOT NULL REFERENCES pilotos(id),
                inicio TEXT NOT NULL,
                fim TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status = 'AGENDADO')
            );
        """)

    def buscar_aeronave(self, aeronave_id):
        return self.connection.execute(
            "SELECT * FROM aeronaves WHERE id = ?", (aeronave_id,)
        ).fetchone()

    def tem_conflito(self, aeronave_id, inicio, fim):
        return self.connection.execute(
            """SELECT 1 FROM agendamentos
               WHERE aeronave_id = ? AND inicio < ? AND fim > ?""",
            (aeronave_id, fim, inicio),
        ).fetchone() is not None

    def inserir_agendamento(self, aeronave_id, piloto_id, inicio, fim):
        cursor = self.connection.execute(
            """INSERT INTO agendamentos
               (aeronave_id, piloto_id, inicio, fim, status)
               VALUES (?, ?, ?, ?, 'AGENDADO')""",
            (aeronave_id, piloto_id, inicio, fim),
        )
        return cursor.lastrowid

    def close(self):
        self.connection.close()
