CREATE TABLE instruments (
    instrument_id INT PRIMARY KEY AUTO_INCREMENT,
    exchange VARCHAR(10),
    name VARCHAR(50),
    segment VARCHAR(20),
    instrument_token INT UNIQUE,
    instrument_type VARCHAR(10),
    strike DECIMAL(10, 2),
    expiry DATE
);

CREATE TABLE vega_vomma (
    calculation_id INT PRIMARY KEY AUTO_INCREMENT,
    instrument_token INT,
    date DATETIME,
    ce_vega DECIMAL(10, 2),
    pe_vega DECIMAL(10, 2),
    ce_vomma DECIMAL(10, 2),
    pe_vomma DECIMAL(10, 2),
    FOREIGN KEY (instrument_token) REFERENCES instruments(instrument_token)
);