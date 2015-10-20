# Requirements

flask
jsonrpc (from: http://json-rpc.org/wiki/python-json-rpc)

# alexandria-trade

Running the API

$ export TRADE_API_SETTINGS=/path/to/trade_api_settings.cfg
$ python trade-api.py
 * Running on http://127.0.0.1:5000/

# bitcoin.conf

Set up the wrapper files with the correct settings.

```
walletnotify=process_incoming_wrapper %s
blocknotify=process_block_wrapper %s
```

"blocknotify" runs when a new block is received on the Bitcoin network.  The argument passed through is the block hash.

"walletnotify" runs when an incoming wallet transaction is received on the Bitcoin network.  The argument passed through is the transaction ID.

# process_receive_wrapper

Set this to run via Cron.

This calls the process_receive.py which will then:
Processes the "receive" table and logs to "action" table. Checks x number of confirmations on receive.

NOTE: Do NOT set the number of confirmations to 0 as this very dangerous due to transaction malleability which WILL cause a double spend.

