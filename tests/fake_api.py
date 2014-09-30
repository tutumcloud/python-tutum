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


def fake_auth():
    status_code = 200
    resp = '{"meta": {"limit": 25, "next": null, "offset": 0, "previous": null, "total_count": 1},' \
           '"objects": [{"key": "%s", "username": "%s"}]}' % (FAKE_APIKEY, FAKE_USER)
    return status_code, json.loads(resp)


def fake_action_list():
    status_code = 200
    resp = '{"meta": {"limit": 25, "next": null, "offset": 0, "previous": null, "total_count": 3}, ' \
           '"objects": [{"action": "Node Cluster Create", "end_date": "Mon, 29 Sep 2014 15:40:59 +0000", "ip": "207.41.188.212", "location": "New York, United States", "method": "POST", "object": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "path": "/api/v1/nodecluster/", "resource_uri": "/api/v1/action/7f62b667-2693-420a-ad2e-41cda5605322/", "start_date": "Mon, 29 Sep 2014 15:40:59 +0000", "state": "Success", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "7f62b667-2693-420a-ad2e-41cda5605322"}, ' \
           '{"action": "Node Cluster Deploy", "end_date": "Mon, 29 Sep 2014 15:41:01 +0000", "ip": "207.41.188.212", "location": "New York, United States", "method": "POST", "object": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "path": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/deploy/", "resource_uri": "/api/v1/action/db69b048-3bab-4a2e-bcbd-91265edf1a31/", "start_date": "Mon, 29 Sep 2014 15:41:00 +0000", "state": "Failed", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "db69b048-3bab-4a2e-bcbd-91265edf1a31"}, ' \
           '{"action": "Node Deploy", "end_date": "Mon, 29 Sep 2014 15:41:16 +0000", "ip": "207.41.188.212", "location": "New York, United States", "method": "POST", "object": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/", "path": "/api/v1/node/fa9df19a-162b-45b4-bb5a-152dfd1b133f/deploy/", "resource_uri": "/api/v1/action/ce9ae16b-88fa-4be6-b12e-fc970b8d2445/", "start_date": "Mon, 29 Sep 2014 15:41:16 +0000", "state": "Failed", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "ce9ae16b-88fa-4be6-b12e-fc970b8d2445"}]}'
    return status_code, json.loads(resp)

def fake_action_fetch():
    status_code = 200
    resp = '{"action": "Node Cluster Create", "end_date": "Mon, 29 Sep 2014 15:40:59 +0000", "ip": "207.41.188.212", "location": "New York, United States", "logs": "", "method": "POST", "object": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "path": "/api/v1/nodecluster/", "resource_uri": "/api/v1/action/7f62b667-2693-420a-ad2e-41cda5605322/", "start_date": "Mon, 29 Sep 2014 15:40:59 +0000", "state": "Success", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36", "uuid": "7f62b667-2693-420a-ad2e-41cda5605322"}'
    return status_code, json.loads(resp)

def fake_provider_list():
    status_code = 200
    resp ='{"meta": {"limit": 25, "next": null, "offset": 0, "previous": null, "total_count": 1}, "objects": [{"available": true, "label": "Digital Ocean", "name": "digitalocean", "regions": ["/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/ams3/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/sgp1/"], "resource_uri": "/api/v1/provider/digitalocean/"}]}'
    return status_code, json.loads(resp)

def fake_provider_fetch():
    status_code = 200
    resp = '{"available": true, "label": "Digital Ocean", "name": "digitalocean", "regions": ["/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/ams3/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/sgp1/"], "resource_uri": "/api/v1/provider/digitalocean/"}'
    return status_code, json.loads(resp)

def fake_region_list():
    status_code = 200
    resp = '{"meta": {"limit": 25, "next": null, "offset": 0, "previous": null, "total_count": 8}, ' \
           '"objects": [{"availability_zones": [], "available": true, "label": "Amsterdam 1", "name": "ams1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/"], "resource_uri": "/api/v1/region/digitalocean/ams1/"}, ' \
           '{"availability_zones": [], "available": true, "label": "San Francisco 1", "name": "sfo1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/sfo1/"}, ' \
           '{"availability_zones": [], "available": true, "label": "New York 2", "name": "nyc2", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/nyc2/"}, ' \
           '{"availability_zones": [], "available": true, "label": "Amsterdam 2", "name": "ams2", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/ams2/"}, ' \
           '{"availability_zones": [], "available": true, "label": "Singapore 1", "name": "sgp1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/sgp1/"}, ' \
           '{"availability_zones": [], "available": true, "label": "London 1", "name": "lon1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/lon1/"}, ' \
           '{"availability_zones": [], "available": true, "label": "New York 3", "name": "nyc3", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/nyc3/"}, ' \
           '{"availability_zones": [], "available": true, "label": "Amsterdam 3", "name": "ams3", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/", "/api/v1/nodetype/digitalocean/32gb/", "/api/v1/nodetype/digitalocean/48gb/", "/api/v1/nodetype/digitalocean/64gb/"], "resource_uri": "/api/v1/region/digitalocean/ams3/"}]}'
    return status_code, json.loads(resp)

def fake_region_fetch():
    status_code = 200
    resp = '{"availability_zones": [], "available": true, "label": "Amsterdam 1", "name": "ams1", "node_types": ["/api/v1/nodetype/digitalocean/512mb/", "/api/v1/nodetype/digitalocean/1gb/", "/api/v1/nodetype/digitalocean/2gb/", "/api/v1/nodetype/digitalocean/4gb/", "/api/v1/nodetype/digitalocean/8gb/", "/api/v1/nodetype/digitalocean/16gb/"], "provider": "/api/v1/provider/digitalocean/", "resource_uri": "/api/v1/region/digitalocean/ams1/"}'
    return status_code, json.loads(resp)

def fake_nodetype_list():
    status_code = 200
    resp = '{"meta": {"limit": 25, "next": null, "offset": 0, "previous": null, "total_count": 9}, ' \
           '"objects": [{"availability_zones": [], "available": true, "label": "512MB", "name": "512mb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/512mb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "1GB", "name": "1gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/1gb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "2GB", "name": "2gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/2gb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "4GB", "name": "4gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/4gb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "8GB", "name": "8gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/8gb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "16GB", "name": "16gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/16gb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "32GB", "name": "32gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/32gb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "48GB", "name": "48gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/48gb/"}, ' \
           '{"availability_zones": [], "available": true, "label": "64GB", "name": "64gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/64gb/"}]}'
    return status_code, json.loads(resp)

def fake_nodetype_fetch():
    status_code = 200
    resp = '{"availability_zones": [], "available": true, "label": "8GB", "name": "8gb", "provider": "/api/v1/provider/digitalocean/", "regions": ["/api/v1/region/digitalocean/nyc1/", "/api/v1/region/digitalocean/ams1/", "/api/v1/region/digitalocean/sfo1/", "/api/v1/region/digitalocean/nyc2/", "/api/v1/region/digitalocean/ams2/", "/api/v1/region/digitalocean/sgp1/", "/api/v1/region/digitalocean/lon1/", "/api/v1/region/digitalocean/nyc3/", "/api/v1/region/digitalocean/ams3/"], "resource_uri": "/api/v1/nodetype/digitalocean/8gb/"}'
    return status_code, json.loads(resp)

def fake_nodeclster_list():
    status_code = 200
    resp = '{"meta": {"limit": 25, "next": null, "offset": 0, "previous": null, "total_count": 2}, ' \
           '"objects": [{"current_num_nodes": 1, "deployed_datetime": "Mon, 29 Sep 2014 22:29:03 +0000", "destroyed_datetime": null, "name": "test", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "region": "/api/v1/region/digitalocean/sfo1/", "resource_uri": "/api/v1/nodecluster/a02c3763-e639-46fc-a6db-587f4dbb5444/", "state": "Deployed", "target_num_nodes": 1, "uuid": "a02c3763-e639-46fc-a6db-587f4dbb5444"}, ' \
           '{"current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "test2", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "state": "Deploying", "target_num_nodes": 1, "uuid": "b616a720-6684-42c6-83bb-4d298b11b3f3"}]}'
    return status_code, json.loads(resp)

def fake_nodecluster_fetch():
    status_code = 200
    resp = '{"actions": ["/api/v1/action/bf02b00a-e2fc-4098-8b69-1424b659ef4a/", "/api/v1/action/f8dce6d4-5c41-46a9-9754-baa8f3cdf031/"], "current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "test2", "node_type": "/api/v1/nodetype/digitalocean/512mb/", "nodes": ["/api/v1/node/43b5ebaf-5b9c-4ed3-a1e5-3d91cea70456/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/b616a720-6684-42c6-83bb-4d298b11b3f3/", "state": "Init", "target_num_nodes": 1, "uuid": "b616a720-6684-42c6-83bb-4d298b11b3f3"}'
    return status_code, json.loads(resp)

def fake_nodecluster_save():
    status_code = 201
    resp = '{"actions": ["/api/v1/action/f47e26a6-c60c-416f-a0a9-ddf14e3aae83/"], "current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "my_cluster", "node_type": "/api/v1/nodetype/digitalocean/1gb/", "nodes": ["/api/v1/node/2cfe7823-f551-4c7b-a82c-f6ab31d7ca25/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/e7915a74-618b-4908-9189-dce965465702/", "state": "Init", "target_num_nodes": 1, "uuid": "e7915a74-618b-4908-9189-dce965465702"}'
    return status_code, json.loads(resp)

def fake_nodecluster_deploy():
    status_code = 202
    resp = '{"actions": ["/api/v1/action/f47e26a6-c60c-416f-a0a9-ddf14e3aae83/", "/api/v1/action/d110016e-e65d-4ce7-9f11-50c6302494a6/"], "current_num_nodes": 1, "deployed_datetime": null, "destroyed_datetime": null, "name": "my_cluster", "node_type": "/api/v1/nodetype/digitalocean/1gb/", "nodes": ["/api/v1/node/2cfe7823-f551-4c7b-a82c-f6ab31d7ca25/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/e7915a74-618b-4908-9189-dce965465702/", "state": "Deploying", "target_num_nodes": 1, "uuid": "e7915a74-618b-4908-9189-dce965465702"}'
    return status_code, json.loads(resp)

def fake_nodecluster_delete():
    status_code = 202
    resp = '{"actions": ["/api/v1/action/f47e26a6-c60c-416f-a0a9-ddf14e3aae83/", "/api/v1/action/d110016e-e65d-4ce7-9f11-50c6302494a6/", "/api/v1/action/e33b4bb1-192b-46a6-a1ba-eadfc494c2dd/"], "current_num_nodes": 1, "deployed_datetime": "Mon, 29 Sep 2014 23:45:45 +0000", "destroyed_datetime": null, "name": "my_cluster", "node_type": "/api/v1/nodetype/digitalocean/1gb/", "nodes": ["/api/v1/node/2cfe7823-f551-4c7b-a82c-f6ab31d7ca25/"], "region": "/api/v1/region/digitalocean/lon1/", "resource_uri": "/api/v1/nodecluster/e7915a74-618b-4908-9189-dce965465702/", "state": "Terminating", "target_num_nodes": 0, "uuid": "e7915a74-618b-4908-9189-dce965465702"}'
    return status_code, json.loads(resp)