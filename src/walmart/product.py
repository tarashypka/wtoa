import playhouse.postgres_ext as pg

from local.peewee.db import db
from local.peewee.db import persist
from local.utils import curr_datetime


class WalmartDepartment(pg.Model):
    """
    Walmart department model to be persisted via peewee ORM.

    Parameters
    ----------
    id : str
        Absolute id starting from root department.
        F.e '3944_401121_134532'.
        Here '134532' is relative department of this id
        and '3944' is parent root department id.
    title : str
        Department title. F.e 'Auto Paint'.
    path : str
        Absolute path starting from root department.
        F.e 'Auto & Tires/Auto Boyd/Auto Paint'.
    parent : str
        Parent department id, None if department is root.
    conflict_ids : [str]
        One department may have multiple ids.
        Field could be used to prevent duplicates.
    updated_at : str
        Last update date and time.
    """
    id = pg.TextField(primary_key=True)
    title = pg.TextField()
    path = pg.TextField()
    parent = pg.ForeignKeyField('self', null=True)
    conflict_ids = pg.ArrayField(pg.TextField, null=True)
    updated_at = pg.DateTimeField(default=curr_datetime())

    class Meta:
        database = db
        db_table = 'wdepartment'

    def __str__(self):
        return str(vars(self)['_data'])

    @db.atomic()
    def persist(self, parent=False):
        """
        Persist department model.

        Parameters
        ----------
        parent : bool
            True to persist all parent departments, False otherwise.

        Returns
        -------
        bool
            True if model was persisted, False otherwise.
        """
        if parent:  # Also persist all parent departments
            depts = []
            parent_dept = self.parent
            while parent_dept:
                depts.append(parent_dept)
                parent_dept = parent_dept.parent
            while depts:
                persist(depts.pop())
        return persist(self)

    @db.atomic()
    def update_(self, **kwargs):
        """
        Update department model.

        Parameters
        ----------
        **kwargs
            Parameters names with their new values.

        Returns
        -------
        int
            # of rows that were modified.
        """
        dept_t = WalmartDepartment
        update_q = dept_t.update(
            **kwargs, updated_at=curr_datetime()
        ).where(dept_t.id == self.id)
        return update_q.execute()
