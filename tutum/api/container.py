from http import send_request

def list_containers():
    """
    Returns a list of Container objects for the given apikey.
    """
    containers = []
    json = send_request('GET', '/container')
    if json:
        json_objects = json.get('objects', [])
        for obj in json_objects:
            containers.append(Container(obj))
    return containers

class Container(object):
    """
    Tutum Container Object.
    """
    def __init__(self, json={}):
        for k, v in json.items():
            setattr(self, k, v)