import requests

from walmart.credentials import API_KEY
from walmart.product import WalmartDepartment
from local.utils import default_logger


logger = default_logger(__name__)


# ----- Constant Values and Helper Functions ----- #


URL_BASE = 'http://api.walmartlabs.com/v1'
URL_TAXONOMY = URL_BASE + '/taxonomy?apiKey=%s&' % API_KEY
REQ_OK = 200


def _req_json(req_url):
    """
    Provide response in dictionary format.

    Parameters
    ----------
    req_url : str
        API url.

    Returns
    -------
    (dict, True)
        In case json was retrieved from response.
    (None, False)
        In case json could not be retrieved from reponse.

    Raises
    ------
    ValueError
        In case of invalid response with status code 400, 403, etc.
    """
    resp = requests.get(req_url)
    if resp.status_code != REQ_OK:
        logger.error('%s:\n%s' % (resp.status_code, resp.text))
        raise ValueError('Invalid response')
    try:
        resp_d = resp.json()
    except Exception:
        return None, resp.status_code
    else:
        return resp_d, resp.status_code


# ----- Find all possible departments and their subdepartments ----- #


def _req_depts():
    """
    Use Taxonomy API to retrieve all departments with their subdepartments.
    Consider https://developer.walmartlabs.com/docs/read/Taxonomy_API
    """
    return _req_json(URL_TAXONOMY)

def _json_to_dept(dept_json):
    """
    Parse department from Taxonomy API json response.

    Parameters
    ----------
    dept_json : dict
        Department from Taxonomy API response.

    Returns
    -------
    WalmartDepartment
        Parsed department.
    """
    id_ = dept_json['id']
    title = dept_json['name']
    path = dept_json['path']
    return WalmartDepartment(id=id_, title=title, path=path)

def _depts_from(dept_jsons, parent=None):
    """
    Recursively parse and yield departments, their subdepartments
    from Taxonomy API json response.

    Parameters
    ----------
    dept_jsons : [dict]
        Departments from Taxonomy API response.
    parent : WalmartDepartment
        department that dept_jsons departments are subdepartments of,
        None if dept_jsons contains root departments.

    Yields
    ------
    WalmartDepartment
        Department or subdepartment found in dept_jsons.
    """
    for dept_json in dept_jsons:
        dept = _json_to_dept(dept_json)
        dept.parent = parent
        yield dept
        try:
            child_depts = dept_json['children']
        except KeyError:
            pass
        else:
            yield from _depts_from(child_depts, parent=dept)


def find_depts():
    """
    Retrieve departments and their subdepartments via Taxonomy API.

    Yields
    ------
    WalmartDepartment
        Departments with all their subdepartments.

    Raises
    ------
    ValueError
        In case of invalid response.
    """
    resp, found = _req_depts()
    if not found:
        raise ValueError('Invalid json in response!')
    else:
        root_depts = resp['categories']
        logger.info('There are %s root depts', len(root_depts))
        return _depts_from(root_depts)
