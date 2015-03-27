-- cat create_table.sql | sqlite3 alexandria_payment.db

CREATE TABLE sendreceivemap (
    id INTEGER PRIMARY KEY ASC,
    currencyA VARCHAR(10),
    addressA VARCHAR(64),
    currencyB VARCHAR(10),
    addressB VARCHAR(64));

CREATE TABLE receive (
    id INTEGER PRIMARY KEY ASC,
    currencyA VARCHAR(10),
    addressA VARCHAR(64),
    amount DECIMAL(16,8),
    confirmations INT,
    txid VARCHAR(128),
    blockhash VARCHAR(128),
    processed BOOLEAN);

CREATE TABLE action (
    id INTEGER PRIMARY KEY ASC,
    txid VARCHAR(128),
    status VARCHAR(128),
    action VARCHAR(128));

