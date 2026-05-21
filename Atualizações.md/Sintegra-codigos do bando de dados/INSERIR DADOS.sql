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