CREATE TABLE logs (
    id_logs INT IDENTITY(1,1) PRIMARY KEY,
    acao VARCHAR(50),              
    status VARCHAR(20),            
    data_hora DATETIME
);