CREATE table IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE table IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    price INTEGER NOT NULL
);

CREATE table IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    status INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE table IF NOT EXISTS orders_items (
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

CREATE TRIGGER order_update_trigger 
AFTER UPDATE ON orders FOR EACH ROW
BEGIN
    UPDATE orders
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = old.id;
END;

INSERT INTO customers(id, name) VALUES (1, "Abhishek");
INSERT INTO customers(id, name) VALUES (2, "Choudhary");

INSERT INTO items(id, name, price) VALUES (1, "Khaana", 100);
INSERT INTO items(id, name, price) VALUES (2, "Peena", 50);
INSERT INTO items(id, name, price) VALUES (3, "Meetha", 25);

INSERT INTO orders(id, customer_id) VALUES (1, 1);
INSERT INTO orders_items(order_id, item_id) VALUES (1, 1);
INSERT INTO orders_items(order_id, item_id) VALUES (1, 3);

INSERT INTO orders(id, customer_id) VALUES (2, 2);
INSERT INTO orders_items(order_id, item_id) VALUES (2, 2);
INSERT INTO orders_items(order_id, item_id) VALUES (2, 3);
