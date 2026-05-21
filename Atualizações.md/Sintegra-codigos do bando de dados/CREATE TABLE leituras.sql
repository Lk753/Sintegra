CREATE TABLE leituras (
    id_leitura INT IDENTITY(1,1) PRIMARY KEY,
    id_sensor INT,
    valor FLOAT,
    data_hora DATETIME,
    CONSTRAINT FK_SensorLeitura FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor)
);