CREATE TABLE alertas (
    id_alerta INT IDENTITY(1,1) PRIMARY KEY,
    id_leitura INT,
    nivel VARCHAR(20),
    mensagem VARCHAR(100),
    data_hora DATETIME,
    CONSTRAINT FK_LeituraAlerta FOREIGN KEY (id_leitura) REFERENCES leituras(id_leitura)
);