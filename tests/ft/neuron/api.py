import sys
import inspect

import requests
import neuron.config as config
import neuron.error as error


def gen_check(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        assert 200 == response.status_code
        assert error.NEU_ERR_SUCCESS == response.json()['error']
        return response
    wrapper.__name__ = f"{func.__name__}_check"
    wrapper.__signature__ = inspect.signature(func)
    current_module = sys.modules[__name__]
    setattr(current_module, wrapper.__name__, wrapper)
    return func


def login(user='admin', password='0000'):
    return requests.post(url=config.BASE_URL + '/api/v2/login', json={"name": user, "pass": password})


def change_password(new_password, user='admin', old_password='0000', jwt=config.default_jwt):
    return requests.post(url=config.BASE_URL + '/api/v2/password', headers={"Authorization": jwt}, json={"name": user, "old_pass": old_password, "new_pass": new_password})


@gen_check
def get_hwtoken(jwt=config.default_jwt):
    return requests.get(url=config.BASE_URL + '/api/v2/hwtoken', headers={"Authorization": jwt})


@gen_check
def get_license(jwt=config.default_jwt):
    return requests.get(url=config.BASE_URL + '/api/v2/license', headers={"Authorization": jwt})


@gen_check
def upload_license(license, jwt=config.default_jwt):
    return requests.post(url=config.BASE_URL + '/api/v2/license', headers={"Authorization": jwt}, json={"license": license})


@gen_check
def upload_virtual_license(license, jwt=config.default_jwt):
    return requests.post(url=config.BASE_URL + '/api/v2/license/virtual', headers={"Authorization": jwt}, json={"license": license})


@gen_check
def delete_virtual_license(jwt=config.default_jwt):
    return requests.delete(url=config.BASE_URL + '/api/v2/license/virtual', headers={"Authorization": jwt})


@gen_check
def change_log_level(json, jwt=config.default_jwt):
    return requests.put(url=config.BASE_URL + '/api/v2/log/level', headers={"Authorization": jwt}, json=json)


@gen_check
def add_node(node, plugin, jwt=config.default_jwt):
    return requests.post(url=config.BASE_URL + '/api/v2/node', headers={"Authorization": jwt}, json={"name": node, "plugin": plugin})


@gen_check
def del_node(node, jwt=config.default_jwt):
    return requests.delete(url=config.BASE_URL + '/api/v2/node', headers={"Authorization": jwt}, json={"name": node})


def get_nodes(type, jwt=config.default_jwt):
    return requests.get(url=config.BASE_URL + '/api/v2/node', headers={"Authorization": jwt}, params={"type": type})


@gen_check
def node_ctl(node, ctl, jwt=config.default_jwt):
    return requests.post(url=config.BASE_URL + '/api/v2/node/ctl', headers={"Authorization": jwt}, json={"node": node, "cmd": ctl})


def get_nodes_state(node, jwt=config.default_jwt):
    return requests.get(url=config.BASE_URL + '/api/v2/node/state', headers={"Authorization": jwt}, params={"node": node})


@gen_check
def node_setting(node, json, jwt=config.default_jwt):
    return requests.post(url=config.BASE_URL + '/api/v2/node/setting', headers={"Authorization": jwt}, json={"node": node, "params": json})


def get_node_setting(node, jwt=config.default_jwt):
    return requests.get(url=config.BASE_URL + '/api/v2/node/setting', headers={"Authorization": jwt}, params={"node": node})


@gen_check
def add_group(node, group, interval=100):
    return requests.post(url=config.BASE_URL + '/api/v2/group', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "interval": interval})


@gen_check
def del_group(node, group):
    return requests.delete(url=config.BASE_URL + '/api/v2/group', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group})


@gen_check
def update_group(node, group, new_name="", interval=0):
    if len(new_name) > 0 and interval > 0:
        return requests.put(url=config.BASE_URL + '/api/v2/group', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "new_name": new_name, "interval": interval})
    elif len(new_name) > 0:
        return requests.put(url=config.BASE_URL + '/api/v2/group', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "new_name": new_name})
    elif interval > 0:
        return requests.put(url=config.BASE_URL + '/api/v2/group', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "interval": interval})
    else:
        assert False


@gen_check
def get_group():
    return requests.get(url=config.BASE_URL + '/api/v2/group', headers={"Authorization": config.default_jwt})


@gen_check
def add_tags(node, group, tags):
    return requests.post(url=config.BASE_URL + '/api/v2/tags', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "tags": tags})


@gen_check
def add_gtags(node, groups):
    return requests.post(url=config.BASE_URL + '/api/v2/gtags', headers={"Authorization": config.default_jwt}, json={"node": node, "groups": groups})


@gen_check
def del_tags(node, group, tags):
    return requests.delete(url=config.BASE_URL + '/api/v2/tags', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "tags": tags})


@gen_check
def update_tags(node, group, tags):
    return requests.put(url=config.BASE_URL + '/api/v2/tags', headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "tags": tags})


def get_tags(node, group):
    return requests.get(url=config.BASE_URL + "/api/v2/tags", headers={"Authorization": config.default_jwt}, params={"node": node, "group": group})


def read_tags(node, group, sync=False):
    return requests.post(url=config.BASE_URL + "/api/v2/read", headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "sync": sync})


def read_tag(node, group, tag, sync=False):
    response = read_tags(node, group, sync)
    assert 200 == response.status_code
    x = list(filter(lambda x: x['name'] == tag,
                    response.json()['tags']))
    assert len(x) == 1
    try:
        x[0]['value']
    except KeyError:
        print(x[0])
    finally:
        return x[0]['value']

def read_tag_error(node, group, tag, sync=False):
    response = read_tags(node, group, sync)
    assert 200 == response.status_code
    x = list(filter(lambda x: x['name'] == tag,
                    response.json()['tags']))
    assert len(x) == 1
    try:
        x[0]['error']
    except KeyError:
        print(x[0])
    finally:
        return x[0]['error']


def read_tag_err(node, group, tag, sync=False):
    response = read_tags(node, group, sync)
    assert 200 == response.status_code
    x = list(filter(lambda x: x['name'] == tag,
                    response.json()['tags']))
    assert len(x) == 1
    try:
        x[0]['error']
    except KeyError:
        print(x[0])
    finally:
        return x[0]['error']


@gen_check
def write_tag(node, group, tag, value):
    return requests.post(url=config.BASE_URL + "/api/v2/write", headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "tag": tag, "value": value})


@gen_check
def write_tags(node, group, tag_values):
    return requests.post(url=config.BASE_URL + "/api/v2/write/tags", headers={"Authorization": config.default_jwt}, json={"node": node, "group": group, "tags": tag_values})

def write_gtags(json):
    return requests.post(url=config.BASE_URL + "/api/v2/write/gtags", headers={"Authorization": config.default_jwt}, json=json)


def add_plugin(library_name, so_file, schema_file):
    return requests.post(url=config.BASE_URL + "/api/v2/plugin", json={"library": library_name, "so_file": so_file, "schema_file": schema_file}, headers={"Authorization": config.default_jwt})


def updata_plugin(library_name, so_file, schema_file):
    return requests.put(url=config.BASE_URL + "/api/v2/plugin", json={"library": library_name, "so_file": so_file, "schema_file": schema_file}, headers={"Authorization": config.default_jwt})


def del_plugin(plugin_name):
    return requests.delete(url=config.BASE_URL + "/api/v2/plugin", json={"plugin": plugin_name}, headers={"Authorization": config.default_jwt})


def get_plugins():
    return requests.get(url=config.BASE_URL + "/api/v2/plugin", headers={"Authorization": config.default_jwt})


@gen_check
def add_template(name, plugin, groups=[]):
    return requests.post(url=config.BASE_URL + "/api/v2/template", json={"name": name, "plugin": plugin, "groups": groups}, headers={"Authorization": config.default_jwt})


@gen_check
def del_template(name):
    return requests.delete(url=config.BASE_URL + "/api/v2/template" + f"?name={name}", headers={"Authorization": config.default_jwt})


@gen_check
def get_template(name):
    return requests.get(url=config.BASE_URL + "/api/v2/template", headers={"Authorization": config.default_jwt}, params={"name": name})


@gen_check
def get_templates():
    return requests.get(url=config.BASE_URL + "/api/v2/template", headers={"Authorization": config.default_jwt})


@gen_check
def inst_template(name, node):
    return requests.post(url=config.BASE_URL + "/api/v2/template/inst", json={"name": name, "node": node}, headers={"Authorization": config.default_jwt})


@gen_check
def add_template_group(tmpl, group, interval=100):
    return requests.post(url=config.BASE_URL + '/api/v2/template/group', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group, "interval": interval})


@gen_check
def update_template_group(tmpl, group, new_name="", interval=0):
    if len(new_name) > 0 and interval > 0:
        return requests.put(url=config.BASE_URL + '/api/v2/template/group', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group, "new_name": new_name, "interval": interval})
    elif len(new_name) > 0:
        return requests.put(url=config.BASE_URL + '/api/v2/template/group', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group, "new_name": new_name})
    elif interval > 0:
        return requests.put(url=config.BASE_URL + '/api/v2/template/group', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group, "interval": interval})
    else:
        assert False


@gen_check
def del_template_group(tmpl, group):
    return requests.delete(url=config.BASE_URL + '/api/v2/template/group', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group})


@gen_check
def get_template_groups(tmpl):
    return requests.get(url=config.BASE_URL + "/api/v2/template/group", headers={"Authorization": config.default_jwt}, params={"name": tmpl})


@gen_check
def add_template_tags(tmpl, group, tags):
    return requests.post(url=config.BASE_URL + '/api/v2/template/tag', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group, "tags": tags})


@gen_check
def update_template_tags(tmpl, group, tags):
    return requests.put(url=config.BASE_URL + '/api/v2/template/tag', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group, "tags": tags})


@gen_check
def del_template_tags(tmpl, group, tags):
    return requests.delete(url=config.BASE_URL + '/api/v2/template/tag', headers={"Authorization": config.default_jwt}, json={"template": tmpl, "group": group, "tags": tags})


def get_template_tags(tmpl, group, name):
    return requests.get(url=config.BASE_URL + "/api/v2/template/tag", headers={"Authorization": config.default_jwt}, params={"template": tmpl, "group": group, "name": name})

def subscribe_group(app, driver, group):
    return requests.post(url=config.BASE_URL + "/api/v2/subscribe", headers={"Authorization": config.default_jwt}, json={"app": app, "driver": driver, "group": group})

def subscribe_groups(app, groups):
    return requests.post(url=config.BASE_URL + "/api/v2/subscribes", headers={"Authorization": config.default_jwt}, json={"app": app, "groups": groups})

def unsubscribe_group(app, driver, group):
    return requests.delete(url=config.BASE_URL + "/api/v2/subscribe", headers={"Authorization": config.default_jwt}, json={"app": app, "driver": driver, "group": group})

def get_metrics(category="global", node=""):
    return requests.get(url=config.BASE_URL + "/api/v2/metrics?category=" + category + "&node=" + node, headers={"Authorization": config.default_jwt})

def get_global_config():
    return requests.get(url=config.BASE_URL + "/api/v2/global/config", headers={"Authorization": config.default_jwt})

def put_global_config(json):
    return requests.put(url=config.BASE_URL + "/api/v2/global/config", headers={"Authorization": config.default_jwt}, json=json)

def get_plugin_schema(plugin):
    return requests.get(url=config.BASE_URL + "/api/v2/schema?schema_name=" + plugin, headers={"Authorization": config.default_jwt})

def get_plugin():
    return requests.get(url=config.BASE_URL + "/api/v2/plugin", headers={"Authorization": config.default_jwt})

def get_version():
    return requests.get(url=config.BASE_URL + "/api/v2/version", headers={"Authorization": config.default_jwt})

def post_ndriver_map(ndriver, driver, group):
    return requests.post(url=config.BASE_URL + "/api/v2/ndriver/map", headers={"Authorization": config.default_jwt}, json={"ndriver": ndriver, "driver": driver, "group":group})

def delete_ndriver_map(ndriver, driver, group):
    return requests.delete(url=config.BASE_URL + "/api/v2/ndriver/map", headers={"Authorization": config.default_jwt}, json={"ndriver": ndriver, "driver": driver, "group":group})

def get_ndriver_map(ndriver):
    return requests.get(url=config.BASE_URL + "/api/v2/ndriver/map?ndriver=" + ndriver, headers={"Authorization": config.default_jwt})

def put_ndriver_tag_param(json):
    return requests.put(url=config.BASE_URL + "/api/v2/ndriver/tag/param", headers={"Authorization": config.default_jwt}, json=json)

def put_ndriver_tag_info(json):
    return requests.put(url=config.BASE_URL + "/api/v2/ndriver/tag/info", headers={"Authorization": config.default_jwt}, json=json)

def get_ndriver_tag(ndriver, driver, group):
    return requests.get(url=config.BASE_URL + "/api/v2/ndriver/tag?ndriver=" + ndriver + "&driver=" + driver + "&group=" + group, headers={"Authorization": config.default_jwt})

# plugin setting


def modbus_tcp_node_setting(node, port, connection_mode=0, transport_mode=0, interval=0, host='127.0.0.1', timeout=3000, max_retries=2):
    return node_setting(node, json={"connection_mode": connection_mode, "transport_mode": transport_mode, "interval": interval,
                                    "host": host, "port": port, "timeout": timeout, "max_retries": max_retries})


def modbus_rtu_node_setting(node, port, connection_mode=0, transport_mode=0, interval=10, host='127.0.0.1', timeout=3000, max_retries=2, link=1, device="", stop=0, parity=0, baud=4, data=3):
    return node_setting(node, json={"connection_mode": connection_mode, "transport_mode": transport_mode,
                                    "interval": interval, "host": host, "port": port, "timeout": timeout,
                                    "max_retries": max_retries, "link": link, "device": device, "stop": stop,
                                    "parity": parity, "baud": baud, "data": data})

def mqtt_node_setting(node):
    return node_setting(node, json={"client-id": "neuron_aBcDeF", "qos":0, "format": 0,
                                    "write-req-topic": f"/neuron/{node}/write/req", "write-resp-topic": f"/neuron/{node}/write/resp",
                                    "offline-cache": False, "cache-sync-interval": 100, "host": "broker.emqx.io", "port": 1883, "username": "", "password": "", "ssl": False})