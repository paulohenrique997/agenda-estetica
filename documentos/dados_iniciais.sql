-- Registros fictícios para testes acadêmicos.
INSERT OR IGNORE INTO clientes (id, nome, telefone, email) VALUES
(1, 'Mariana Costa', '(49) 99999-0001', 'mariana.teste@example.com'),
(2, 'Ana Martins', '(49) 99999-0002', 'ana.teste@example.com');

INSERT OR IGNORE INTO profissionais (id, nome, especialidade, telefone) VALUES
(1, 'Carla Souza', 'Estética facial', '(49) 99999-1001'),
(2, 'Fernanda Lima', 'Estética corporal', '(49) 99999-1002');

INSERT OR IGNORE INTO procedimentos (id, nome, descricao, duracao_minutos, valor) VALUES
(1, 'Limpeza de pele', 'Procedimento demonstrativo para testes', 60, 150.00),
(2, 'Massagem modeladora', 'Procedimento demonstrativo para testes', 50, 120.00);
