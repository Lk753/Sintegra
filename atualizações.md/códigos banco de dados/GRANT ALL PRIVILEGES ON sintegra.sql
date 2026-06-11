-- 1. Garante que o usuário miria_admin tenha acesso total especificamente ao banco sintegra
GRANT ALL PRIVILEGES ON sintegra.* TO 'miria_admin'@'localhost';

-- 2. Aplica as novas configurações de permissão imediatamente
FLUSH PRIVILEGES;