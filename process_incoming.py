#!/usr/bin/env python
"""Process incoming wallet transactions and write them to a database"""

import sqlite3
import sys
from jsonrpc import ServiceProxy
import json
import os

txid = sys.argv[1]

rpc_user = os.environ['RPC_USER']
rpc_password = os.environ['RPC_PASSWORD']
rpc_port = os.environ['RPC_PORT']
currency_a = os.environ['CURRENCY_A']

access = ServiceProxy("http://%s:%s@127.0.0.1:%s" % (rpc_user, rpc_password, rpc_port))

transactions = access.listtransactions()

con = None

con = sqlite3.connect('alexandria_payment.db')
    
def add_tx_to_database(tx):
    with con:
        cur = con.cursor()
        # First run a select to see if a receive exists
        cur.execute("SELECT txid FROM receive WHERE txid = ? LIMIT 1;" , (tx['txid'],))
        if not cur.fetchone():
            cur.execute("INSERT INTO receive (currencyA, addressA, amount, txid) VALUES (?, ?, ?, ?);"
                , (currency_a, tx['address'], tx['amount'], tx['txid']))

for tx in transactions:
    if tx['category'] == 'receive' and tx['txid'] == txid:
        add_tx_to_database(tx)

con.close()

