"""JSON utils.

.. code-block:: python

    >>> from utils import jsonx
    >>> data = {'name': 'Alice', 'age': 20}
    >>> file_name = '/tmp/data.json'
    >>> jsonx.write(file_name, data)
    >>> data2 = jsonx.read(file_name)
    >>> data == data2
    True

"""
import json


def read(file_name):
    """Read JSON from file.

    Args:
        file_name (str): file name

    Returns:
        Parsed JSON data

    """
    with open(file_name, 'r') as fin:
        data = json.loads(fin.read())
        fin.close()
    return data


def write(file_name, data):
    """Write data as JSON to file.

    Args:
        file_name (str): file name
        data: data as serializable object

    """
    with open(file_name, 'w') as fout:
        fout.write(json.dumps(data))
        fout.close()
