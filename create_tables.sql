CREATE DATABASE IF NOT EXISTS card_misuse_analytics;
USE card_misuse_analytics;

CREATE TABLE IF NOT EXISTS transactions_standard (
    transaction_id VARCHAR(50),
    customer_id VARCHAR(50),
    transaction_date DATETIME,
    amount DECIMAL(12,2),
    city VARCHAR(50),
    state VARCHAR(50),
    merchant_category VARCHAR(50),
    channel VARCHAR(20),
    is_fraud INT,
    risk_level VARCHAR(20),
    source_file VARCHAR(100)
);
