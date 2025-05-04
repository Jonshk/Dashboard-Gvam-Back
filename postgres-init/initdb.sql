-- initdb.sql

-- Tabla de usuarios (para autenticación)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT
);

-- Tabla de centros
CREATE TABLE IF NOT EXISTS centers (
    id SERIAL PRIMARY KEY,
    center TEXT NOT NULL,
    phonenumber TEXT
);

-- Tabla de stock central
CREATE TABLE IF NOT EXISTS stock (
    id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    min_stock_level INTEGER,
    price REAL,
    image_path TEXT,
    category TEXT,
    estado TEXT
);

-- Tabla de órdenes
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    center_id INTEGER REFERENCES centers(id),
    shipping_company TEXT,
    order_date DATE
);

-- Tabla de ítems de órdenes
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_name TEXT,
    quantity INTEGER
);

-- Tabla de reparaciones
CREATE TABLE IF NOT EXISTS repairs (
    id SERIAL PRIMARY KEY,
    center_id INTEGER REFERENCES centers(id),
    repair_type TEXT,
    repair_date DATE
);

-- Tabla de ítems de reparaciones
CREATE TABLE IF NOT EXISTS repair_items (
    id SERIAL PRIMARY KEY,
    repair_id INTEGER REFERENCES repairs(id),
    product_name TEXT,
    repair_quantity INTEGER
);

-- Tabla de recepciones
CREATE TABLE IF NOT EXISTS receptions (
    id SERIAL PRIMARY KEY,
    center_id INTEGER REFERENCES centers(id),
    reception_date DATE
);

-- Tabla de ítems de recepciones
CREATE TABLE IF NOT EXISTS reception_items (
    id SERIAL PRIMARY KEY,
    reception_id INTEGER REFERENCES receptions(id),
    product_name TEXT,
    quantity INTEGER
);

-- Tabla de inventario por centro
CREATE TABLE IF NOT EXISTS center_stock (
    id SERIAL PRIMARY KEY,
    center_id INTEGER REFERENCES centers(id),
    product_name TEXT,
    quantity INTEGER,
    price REAL,
    image_path TEXT,
    category TEXT,
    estado TEXT
);
