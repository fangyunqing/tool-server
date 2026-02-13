DROP TABLE IF EXISTS tool_order;
DROP TABLE IF EXISTS tool_user;
DROP TABLE IF EXISTS tool_config;

CREATE TABLE IF NOT EXISTS tool_order
(
    id INTEGER PRIMARY KEY,
    code TEXT,
    fee TEXT,
    account_price TEXT,
    add_account_num INTEGER,
    day_price TEXT,
    add_day_num INTEGER,
    order_status INTEGER,
    pay_voucher BLOB,
    create_time TEXT DEFAULT '',
    update_time TEXT DEFAULT '',
    pay_time TEXT DEFAULT '',
    finish_time TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS tool_user
(
    id INTEGER PRIMARY KEY,
    code TEXT,
    life_time TEXT,
    create_time TEXT
);

CREATE TABLE IF NOT EXISTS tool_config
(
    id INTEGER PRIMARY KEY,
    item_name TEXT,
    item_value TEXT
);

CREATE INDEX IF NOT EXISTS idx_tool_order_code ON tool_order(code);
CREATE INDEX IF NOT EXISTS idx_tool_user_code ON tool_user(code);

INSERT INTO tool_config (item_name, item_value)
VALUES ('admin_code', 'c7d540c4-ac37-7b3f-2737-11533e0a1e23');

INSERT INTO tool_config (item_name, item_value)
VALUES ('account_price', '0.2');

INSERT INTO tool_config (item_name, item_value)
VALUES ('day_price', '0.3');

INSERT INTO tool_order (code, add_account_num, add_day_num, order_status, create_time)
VALUES ('1', 1, 1, 1, '2020-01-01 11:11:11')

