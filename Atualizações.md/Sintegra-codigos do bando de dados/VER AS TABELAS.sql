-- Ver a junção de todas as tabelas (Sensores -> Leituras -> Alertas)
SELECT 
    S.nome AS Sensor,
    L.valor AS Valor_Lido,
    L.data_hora AS Data_Leitura,
    A.mensagem AS Alerta_Gerado,
    A.nivel AS Severidade
FROM sensores S
INNER JOIN leituras L ON S.id_sensor = L.id_sensor
LEFT JOIN alertas A ON L.id_leitura = A.id_leitura;