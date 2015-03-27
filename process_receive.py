#!/usr/bin/env python
"""Processes the "receive" table and logs to "action" table. Checks x number of confirmations on receive."""

import sqlite3
import sys
from jsonrpc import ServiceProxy
import json

confirms = int(sys.argv[1])

con = sqlite3.connect('alexandria_payment.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

def process_receive(receive):
    # The core of how we process receiving of a payment
    # Process the receive and then update Processed

    # Magic goes here

    # Log completion
    status = "SENT"
    action = "SEND x AMOUNT TO y ADDRESS"
    cur.execute("INSERT INTO action (txid, status, action) VALUES (?, ?, ?);"
        , (receive['txid'], status, action))
    con.commit()

    # Update the record once it has been Processed
    cur.execute("UPDATE receive SET processed = 1 WHERE txid = ?;", (receive['txid'],))
    con.commit()

# First run a select to see if a receive has been Processed. Exit if it has been Processed.
with con:
    cur.execute("SELECT * FROM receive WHERE processed = 0 AND confirmations >= ?;", (confirms,))
    results = cur.fetchall()

if results:
    for receive in results:
        process_receive(receive)

con.close()

