from requests import get
from xmltodict import parse
from json import loads
from demjson import decode
from pprint import pprint


_default_ip = "192.168.1.254"


class BTHub:
    def __init__(self, ip=_default_ip):
        self.ip = ip

    def data(self):
        data_url = "http://" + self.ip + "/cgi/cgi_owl.js"
        content = str(get(data_url).content)
        data = content.replace("var owl_tplg=", "")
        data = data[0:data.find("addCfg")]
        print(data)

    def devices(self):
        devices_url = "http://" + self.ip + "/nonAuth/home_status.xml"
        data = get_xml_data(devices_url)
        array_from_string(data["status"]["known_device_list"]["@value"])

    def status(self):
        status_url = "http://" + self.ip + "/nonAuth/wan_conn.xml"
        data = get_xml_data(status_url)
        pprint(data)


def get_xml_data(url):
    data = get(url).content
    return parse(data)


def array_from_string(string):
    obj = decode(string)
    pprint(obj)
    return obj
