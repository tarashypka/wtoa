from local.peewee.db import db
from local.peewee.tables import tables


db.connect()
db.create_tables(tables, safe=True)
db.close()
