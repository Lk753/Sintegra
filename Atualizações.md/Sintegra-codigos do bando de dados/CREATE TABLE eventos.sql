CREATE TABLE eventos (
	id_evento INT IDENTITY(1,1) PRIMARY KEY,
    descricao VARCHAR(100),
    data_hora DATETIME
);