CREATE TABLE manutencao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Horario DATETIME DEFAULT CURRENT_TIMESTAMP,
    dispositivo VARCHAR(50),
    evento_manutencao VARCHAR(100) DEFAULT 'Reinicialização do sistema'
);