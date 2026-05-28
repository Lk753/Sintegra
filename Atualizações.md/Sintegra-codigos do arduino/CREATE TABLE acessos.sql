CREATE TABLE acessos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    horario DATETIME DEFAULT CURRENT_TIMESTAMP,
    sensor VARCHAR(50),
    temperatura DECIMAL(5,2),
    ip_origem VARCHAR(45)
);