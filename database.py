import sqlite3


class Database:
    table_name = "siglas_vivver"

    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name}(id INTEGER PRIMARY KEY, sigla TEXT, texto TEXT)")
        self.conn.commit()

    def insert(self, sigla, texto):
        self.cur.execute(f"INSERT INTO {self.table_name} VALUES (NULL, ?, ?)", (sigla, texto))
        self.conn.commit()

    def view(self):
        self.cur.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE id=?", (id,))
        self.conn.commit()

    # fecha a conexão
    def __del__(self):
        self.conn.close()
