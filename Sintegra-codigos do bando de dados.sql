Atualizações.md/Sintegra-codigos do bando de dados/CREATE TABLE alertas.sql

CREATE TABLE alertas (
    id_alerta INT IDENTITY(1,1) PRIMARY KEY,
    id_leitura INT,
    nivel VARCHAR(20),
    mensagem VARCHAR(100),
    data_hora DATETIME,
    CONSTRAINT FK_LeituraAlerta FOREIGN KEY (id_leitura) REFERENCES leituras(id_leitura)
);

Atualizações.md/Sintegra-codigos do bando de dados/CREATE TABLE eventos.sql

CREATE TABLE eventos (
	id_evento INT IDENTITY(1,1) PRIMARY KEY,
    descricao VARCHAR(100),
    data_hora DATETIME
);


Atualizações.md/Sintegra-codigos do bando de dados/CREATE TABLE leituras.sql

CREATE TABLE leituras (
    id_leitura INT IDENTITY(1,1) PRIMARY KEY,
    id_sensor INT,
    valor FLOAT,
    data_hora DATETIME,
    CONSTRAINT FK_SensorLeitura FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor)
);

Atualizações.md/Sintegra-codigos do bando de dados/CREATE TABLE logs.sql

@@ -1,6 +0,0 @@
CREATE TABLE logs (
    id_logs INT IDENTITY(1,1) PRIMARY KEY,
    acao VARCHAR(50),              
    status VARCHAR(20),            
    data_hora DATETIME
);


Atualizações.md/Sintegra-codigos do bando de dados/INSERIR DADOS.sql

-- 1. Limpa os dados antigos e zera os contadores de ID (RESET)
DELETE FROM alertas;
DELETE FROM leituras;
DELETE FROM sensores;
DELETE FROM eventos;
DELETE FROM logs;

DBCC CHECKIDENT ('sensores', RESEED, 0);
DBCC CHECKIDENT ('leituras', RESEED, 0);
DBCC CHECKIDENT ('alertas', RESEED, 0);

SET DATEFORMAT ymd;
GO




INSERT INTO sensores (nome, tipo, localizacao)
VALUES ('DHT11', 'digital', 'ARDUINO');


INSERT INTO leituras (id_sensor, valor, data_hora)
VALUES (1, 1.50, '20250522 14:30:00');


INSERT INTO alertas (id_leitura, nivel, mensagem, data_hora)
VALUES (1, 'alto', 'muito quente', '20250522 14:30:00');


INSERT INTO eventos (descricao, data_hora)
VALUES ('reuniao', '20250522 14:30:00');

INSERT INTO logs (acao, status, data_hora)
VALUES ('fazer log dos sensores', 'ativo', '20250522 14:30:00');


Atualizações.md/Sintegra-codigos do bando de dados/VER AS TABELAS.sql

 Ver a junção de todas as tabelas (Sensores -> Leituras -> Alertas)
SELECT 
    S.nome AS Sensor,
    L.valor AS Valor_Lido,
    L.data_hora AS Data_Leitura,
    A.mensagem AS Alerta_Gerado,
    A.nivel AS Severidade
FROM sensores S
INNER JOIN leituras L ON S.id_sensor = L.id_sensor
LEFT JOIN alertas A ON L.id_leitura = A.id_leitura;

