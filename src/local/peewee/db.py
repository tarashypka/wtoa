import playhouse.postgres_ext as pg

from local.peewee.credentials import PG_DBNAME
from local.peewee.credentials import PG_USERNAME
from local.peewee.credentials import PG_PASSWORD
from local.utils import default_logger


logger = default_logger(__name__)
HOST = '127.0.0.1'


db = pg.PostgresqlExtDatabase(
    database=PG_DBNAME,
    user=PG_USERNAME,
    password=PG_PASSWORD,
    host=HOST,
    register_hstore=False
)


def persist(obj):
    """
    Persist peewee model.

    Parameters
    ----------
    obj : Model
        Object to persist. 
        Should inherit from peewee Model and be preconfigured with database.

    Returns
    -------
    bool
        True if persisted, False otherwise.
    """
    try:
        obj.save(force_insert=True)
    except pg.IntegrityError as err:  # Most likely Duplicate Key violation
        logger.warning(err)
        return False
    else:
        return True
