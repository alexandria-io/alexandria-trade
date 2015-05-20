#!/usr/bin/env python
"""Public API"""

from flask import Flask, g, request
import sqlite3
from jsonrpc import ServiceProxy
import json
import os

app = Flask(__name__)
app.config.from_envvar('TRADE_API_SETTINGS')

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

def get_btc_address():
    access = ServiceProxy("http://%s:%s@127.0.0.1:%s" % (app.config['RPC_USER'], app.config['RPC_PASSWORD'], app.config['RPC_PORT']))
    address = access.getnewaddress()
    return address

def get_flo_balance():
    access = ServiceProxy("http://%s:%s@127.0.0.1:%s" % (app.config['CURRENCY_B_RPC_USER'], app.config['CURRENCY_B_RPC_PASSWORD'], app.config['CURRENCY_B_RPC_PORT']))
    balance = access.getbalance()
    return balance

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/echo")
def echo():
    return "Echo test!"

@app.route('/depositaddress')
def depositaddress():
    """Return a BTC address for deposits to a FLO address"""
    # TODO: Input validation
    # TODO: Get a new BTC deposit address
    if 'currency' in request.args:
        currencyA = request.args['currency']
    else:
        currencyA = 'BTC'
    addressB = request.args['floaddress']

    # First check that an address exists
    get_db().row_factory=sqlite3.Row
    cur = get_db().cursor()
    cur.execute("SELECT * FROM sendreceivemap WHERE addressB = ? LIMIT 1;", (addressB,))
    result = cur.fetchone()
    if not result:
        addressA = get_btc_address()
        #cur.execute("update sendreceivemap set addressB = ? where addressB = "" limit 1;", (addressB,))
        cur.execute("INSERT INTO sendreceivemap (currencyA, addressA, currencyB, addressB) VALUES (?, ?, 'FLO', ?);"
                , (currencyA, addressA, addressB))
        get_db().commit()
    else:
        addressA = result["addressA"]
    return addressA

@app.route('/flobalance')
def flobalance():
    """Return FLO balance"""
    return str(get_flo_balance())

if __name__ == "__main__":

    app.run()

