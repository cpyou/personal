# -*- coding: utf-8 -*-
import requests
import random


import json
import random
import urllib2

HOST = '127.0.0.1'
PORT = 8069
DB = 'zhixian'
USER = 'admin'
PASS = 'pzfresh&oscg'


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    # req = urllib2.Request(url=url, data=json.dumps(data), headers={
    #     "Content-Type":"application/json",
    # })
    # reply = json.load(urllib2.urlopen(req))
    # if reply.get("error"):
    #     raise Exception(reply["error"])
    # return reply["result"]
    r = requests.post(url=url, data=json.dumps(data), headers={
        "Content-Type": "application/json",
    })
    return r.json()['result']


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)

# create a new note
args = {
}

note_id = call(url, "object", "execute", DB, uid, PASS, 'eshop.to.odoo', 'synchronous_method', args)
