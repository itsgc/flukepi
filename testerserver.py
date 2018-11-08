import datetime
import json
import re
import time
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import url_for
from lldp_gen import get_lldp_info
from os import environ
from yaml import load

try:
    import thread
except ImportError:
    import _thread as thread
import time


def create_app():
    app = Flask(__name__)
    return app

app = create_app()
app.app_context().push()

@app.route("/")
def index():
    return "Woosh we have a page!"

@app.route("/lldp")
def lldp():
    payload = get_lldp_info(type='mock')
    # payload =  { 'switch_name': 'hamasw4-1', 'switch_port': 'ge-0/2/45', 'vlans': ['SALES_WIRED', 'VOIP'] }
    return jsonify(payload)

@app.route("/dhcp")
def dhcp():
    payload =  { 'ip_address': '10.20.20.30', 'subnet_mask': '255.255.252.0', 'gateway': '10.20.20.1' }
    return jsonify(payload)

@app.route("/link")
def link():
    payload =  { 'state': 'UP', 'speed': '1000Mb/s', 'Autoneg': 'on', 'duplex': 'full' }
    return jsonify(payload)
