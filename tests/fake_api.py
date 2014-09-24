import requests
import json
import datetime

FAKE_USER = 'fake_tutum_user'
FAKE_PASSWORD = 'fake_tutum_password'
FAKE_APIKEY = 'dff93a893ec78e4305ff57c75721f38bdc8384f6'
FAKE_EMAIL = 'fake@fack.tutum.co'
FAKE_UUID = 'b0374cc2-4003-4270-b131-25fc494ea2be'
FAKE_UUIDS = ['b0374cc2-4003-4270-b131-25fc494ea2be', 'd89fc6f9-d7ec-4602-be94-429c65d6657d',
              'aeaa0b9f-a878-488a-b4a5-a5b54264edd7']


def response(status_code=200, content='', headers=None, reason=None, elapsed=0,
             request=None):
    res = requests.Response()
    res.status_code = status_code
    content = json.dumps(content).encode('ascii')
    res._content = content
    res.headers = requests.structures.CaseInsensitiveDict(headers or {})
    res.reason = reason
    res.elapsed = datetime.timedelta(elapsed)
    res.request = request
    return res


def fake_resp(fake_api_call):
    status_code, content = fake_api_call()
    return response(status_code=status_code, content=content)


def get_fake_auth():
    status_code = 200
    response = {"meta": {"limit": 25, "next": None, "offset": 0, "previous": None, "total_count": 1},
                "objects": [{"key": FAKE_APIKEY, "username": FAKE_USER}]}

    return status_code, response