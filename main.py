#!flask/bin/python
from flask import Flask
import os
from authonticate import Authonticate
from info_host import InfoHost
from ssh_zone import SshZone
from flask import jsonify,json,request

app = Flask(__name__)

class ChangePassword():
    def __init__(self,username,password,instance_id,host=""):
        self.username=username
        self.password=password
        self.instance_id=instance_id
        self.host=host
    
    def change(self):
        self.auth=Authonticate("user","pass")
        info_host = InfoHost(self.instance_id)
        self.zone = info_host.detailHost()
        self.token = self.auth.getToken() 
        ssh = SshZone(self.username,self.password,self.zone,self.instance_id)
        r = ssh.run_command_normally()
        print(r)


class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



@app.route('/v1/server/change_password',methods=['POST'])
def change_password():
    try:
        res = request.get_json()["server"]
        print("request",res)
        server = ChangePassword(res["username"],res["password"],res["instance_id"])
        res = server.change()
        return success_result("success","password changed")

    except Exception as e:
#        return error_result("fail","key error missing %s"%e) 
        raise InvalidUsage(error_result("fail","key error missing %s"%e),status_code=400)


def error_result(status,message):
    results={}
    results["error"]={}
    results["error"]["status"]=status
    results["error"]['message']=message
    return results


def success_result(status,message):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    results["data"]['message']=message
    return jsonify(results)


   

if __name__ == '__main__':
	app.run(host= '0.0.0.0',debug=True,port=8585)
