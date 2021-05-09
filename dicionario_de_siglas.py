import database

db = database.Database('siglas.db')
dicio_siglas = {}

for row in database.Database.view(db):
    dicio_siglas[row[1]] = row[2]

db.conn.close()