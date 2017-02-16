# Search and persist all departments and their subdepartments.
#
# Approximate # of API requests required: 1

from local.utils import default_logger
from walmart.apiuser import find_depts


logger = default_logger('pipeline.1_insert_dept')
n_persisted = 0
for dept in find_depts():
    persisted = dept.persist()
    if persisted:
        n_persisted += 1
logger.info('Persisted %s departments' % n_persisted)
