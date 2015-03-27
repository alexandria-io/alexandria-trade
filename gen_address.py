#!/usr/bin/env python
"""Generate new addresses and write them to a database"""

import sqlite3
import sys
from jsonrpc import ServiceProxy
import json
import os

address_count = int(sys.argv[1])

rpc_user = os.environ['RPC_USER']
rpc_password = os.environ['RPC_PASSWORD']
rpc_port = os.environ['RPC_PORT']
currency_a = os.environ['CURRENCY_A']

access = ServiceProxy("http://%s:%s@127.0.0.1:%s" % (rpc_user, rpc_password, rpc_port))

con = sqlite3.connect('alexandria_payment.db')
    
def add_address_to_database(address):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO sendreceivemap (currencyA, addressA) VALUES (?, ?);", (currency_a, address))
        print address

for count in range(address_count):
    address = access.getnewaddress()
    add_address_to_database(address)

con.close()

