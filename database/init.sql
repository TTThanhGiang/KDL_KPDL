CREATE DATABASE IF NOT EXISTS crypto_db;

USE crypto_db;

CREATE TABLE IF NOT EXISTS coin_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    volume DECIMAL(18, 8) NOT NULL,
    highPrice DECIMAL(18, 8) NOT NULL,
    lowPrice DECIMAL(18, 8) NOT NULL,
    time DATETIME DEFAULT CURRENT_TIMESTAMP
);