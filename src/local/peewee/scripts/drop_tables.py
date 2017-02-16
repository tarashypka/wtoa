from local.peewee.db import db
from local.peewee.tables import tables


db.connect()
db.drop_tables(reversed(tables), safe=True)
db.close()
