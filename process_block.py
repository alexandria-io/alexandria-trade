#!/usr/bin/env python
"""Process incoming block and unprocessed receives and update the database"""

import sqlite3
import sys
from jsonrpc import ServiceProxy
import json

blockhash = sys.argv[1]

rpc_user = os.environ['RPC_USER']
rpc_password = os.environ['RPC_PASSWORD']
rpc_port = os.environ['RPC_PORT']
currency_a = os.environ['CURRENCY_A']

access = ServiceProxy("http://%s:%s@127.0.0.1:%s" % (rpc_user, rpc_password, rpc_port))

transactions = access.listtransactions()

con = sqlite3.connect('alexandria_payment.db')
cur = con.cursor()
    
def process_transaction(tx):
    # First run a select to see if a receive has been Processed. Exit if it has been Processed.
    with con:
        cur.execute("UPDATE receive SET confirmations = ?, blockhash = ? WHERE txid = ?;"
                , (tx['confirmations'], tx['blockhash'], tx['txid']))
        con.commit()

for tx in transactions:
    if tx['category'] == 'receive' and  tx['confirmations'] >= 1:
        process_transaction(tx)

con.close()

