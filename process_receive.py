#!/usr/bin/env python
"""Processes the "receive" table and logs to "action" table. Checks x number of confirmations on receive."""

import sqlite3
import sys
from jsonrpc import ServiceProxy
import json
import requests

confirms = int(sys.argv[1])

con = sqlite3.connect('alexandria_payment.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

def get_bittrex_values():
    url = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-flo'
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "Unable to connect to Bittrex API ;_;"
    m = r.json()['result'][0]
    
    bittrexLastBTCFLO = m['Last']
    bittrexVolumeFLO = m['Volume']
    return bittrexLastBTCFLO, bittrexVolumeFLO

def get_poloniex_values():
    url = 'https://poloniex.com/public?command=returnTradeHistory&currencyPair=BTC_FLO'
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "Unable to connect to Poloniex API ;_;"
    m = r.json()
    poloniexLastBTCFLO = m[0]['rate']

    url = 'https://poloniex.com/public?command=return24hVolume'
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "Unable to connect to Poloniex API ;_;"
    m = r.json()
    poloniexVolumeFLO = m['BTC_FLO']['FLO']

    return float(poloniexLastBTCFLO), float(poloniexVolumeFLO)


def get_cryptsy_values():
    url = 'http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=3'
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "Unable to connect to Cryptsy API ;_;"
    m = r.json()['return']['markets']['LTC']
    cryptsyLastBTCLTC = m['lasttradeprice']

    url = 'http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=61'
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "Unable to connect to Cryptsy API ;_;"
    m = r.json()['return']['markets']['FLO']
    cryptsyLastLTCFLO = m['lasttradeprice']
    cryptsyVolumeFLO = m['volume']

    return float(cryptsyLastBTCLTC), float(cryptsyLastLTCFLO), float(cryptsyVolumeFLO)

def process_receive(receive):
    # The core of how we process receiving of a payment
    # Process the receive and then update Processed

    cryptsyLastBTCLTC, cryptsyLastLTCFLO, cryptsyVolumeFLO  = get_cryptsy_values()
    print "cryptsy last BTC/LTC: %.8f, last: %.8f, volume: %.2f" % (cryptsyLastBTCLTC, cryptsyLastLTCFLO, cryptsyVolumeFLO)
    bittrexLastBTCFLO, bittrexVolumeFLO  = get_bittrex_values()
    print "bittrex last: %.8f, volume: %.2f" % (bittrexLastBTCFLO, bittrexVolumeFLO)
    poloniexLastBTCFLO, poloniexVolumeFLO  = get_poloniex_values()
    print "poloniex last: %.8f, volume: %.2f" % (poloniexLastBTCFLO, poloniexVolumeFLO)

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

