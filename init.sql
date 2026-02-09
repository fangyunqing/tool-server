DROP TABLE IF EXISTS tool_order;
DROP TABLE IF EXISTS tool_user;
DROP TABLE IF EXISTS tool_config;

CREATE TABLE IF NOT EXISTS tool_order
(
    id INTEGER PRIMARY KEY,
    code TEXT,
    add_account_num INTEGER,
    add_day_num INTEGER,
    order_status INTEGER,
    create_time TEXT,
    pay_time TEXT,
    finish_time TEXT
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


