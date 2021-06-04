from flask import Flask, jsonify, request, Response, json, abort
import subprocess as sp
import paramiko
import threading
import time 
from bson.objectid import ObjectId
import sys
import json
import os
import requests
import random
from urllib.parse import unquote
# import threading
'''
sshzone for connect compute for instance password change 

'''
class SshZone():
    def __init__(self,username,password,ipaddress,instance_id,look_for_keys=False,allow_agent=False):
        self.username = username
        self.password = password
        self.ipaddress = ipaddress
        self.instance_id = instance_id
        '''
        this function for run virsh command on compute
        '''
    def run_command_normally(self):
        privateKey = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa") # path of private key
        client = paramiko.SSHClient() # create paramiko client for remote connection to server via ssh
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # default policy set for paramiko client
        errorLogs=[]
        logs=[]
        errorResult="success"
        command="virsh set-user-password --user %s --password %s %s"%(self.username,self.password,self.instance_id)
        print(command)
        try:
            client.connect( hostname = self.ipaddress, port="22", username = "root", pkey = privateKey, timeout=1000, allow_agent=False,look_for_keys=False)
            client.invoke_shell()
            stdin , stdout, stderr = client.exec_command(command,timeout=10000)
            if "cat" in command:
                errorLogs=stderr.readlines()
                logs=stdout.readlines() 
            for i in line_buffered(stdout):
                print(i)
        except paramiko.AuthenticationException as AUTH:
            print(AUTH)
        except paramiko.SSHException as sshException:
            print(sshException)
        except paramiko.ssh_exception.SSHException as timeout:
            print(timeout)
        except Exception as e:
            print(e)
        finally:
            client.close()
        return errorLogs,logs,errorResult
    



# this function used to buffer stdout of remote terminal.
def line_buffered(f):
    line_buf = ""
    while not f.channel.exit_status_ready():
        line_buf = f.readline()
        yield line_buf
        line_buf = ''

# create error result structure
def error_result(status,message):
    results={}
    results["error"]={}
    results["error"]["status"]=status
    results["error"]['message']=message
    return jsonify(results)

# create success result structure
def success_result(status,message,types=""):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    if types !="":
        results["data"]["type"]=types
    results["data"]['message']=message
    return jsonify(results)

# test.runCommand()
