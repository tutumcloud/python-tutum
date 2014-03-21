from http import send_request

def list_containers(username, apikey):
    """
    Returns a list of Container objects for the given apikey.
    """
    json = send_request('GET', '/container', username=username, apikey=apikey)
    json_objects = json.get('objects', [])
    containers = []
    for obj in json_objects:
        instance = Container(obj)
        containers.append(instance)
    return containers

class Container(object):
    """
    Tutum Container Object.
    """
    def __init__(self, json={}):
        for k, v in json.items():
            setattr(self, k, v)