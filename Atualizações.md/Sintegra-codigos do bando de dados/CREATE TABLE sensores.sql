USE Sintegra;

CREATE TABLE sensores (
	id_sensor INT IDENTITY (1,1) PRIMARY KEY,
	nome VARCHAR (50),
	tipo VARCHAR (30),
	localizacao VARCHAR (50)
);
