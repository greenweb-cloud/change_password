
import requests
import json
import time
from authonticate import Authonticate


class InfoHost():
    def __init__(self,instance_id):
        self.instance_id = instance_id

    def getURL(self):
        return "http://ipaddress:8774/v2.1/servers/"

    def detailHost(self):
        self.auth=Authonticate("user","pass")
        header= {"X-Auth-Token":self.auth.getToken(),"Content-Type":"application/json"}
        r = requests.get(self.getURL()+"/%s"%self.instance_id , headers=header,verify=False)
        response=r.json()
        return response["server"]["OS-EXT-SRV-ATTR:host"]




