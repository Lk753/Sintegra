CREATE TABLE Eventos_criticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Horario DATETIME DEFAULT CURRENT_TIMESTAMP,
    sensor VARCHAR(50),
    Temperatura_critica DECIMAL(5,2),
    Mensagem VARCHAR(100) DEFAULT 'ALERTA: Superaquecimento detectado!'
);
