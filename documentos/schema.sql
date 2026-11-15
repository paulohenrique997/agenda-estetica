PRAGMA foreign_keys = ON;

-- Estrutura compatível com os modelos definidos em app.py.

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(120) NOT NULL,
    telefone VARCHAR(30) NOT NULL,
    email VARCHAR(120) UNIQUE
);

CREATE TABLE IF NOT EXISTS profissionais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(120) NOT NULL,
    especialidade VARCHAR(120),
    telefone VARCHAR(30),
    ativo BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS procedimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(120) NOT NULL,
    descricao TEXT,
    duracao_minutos INTEGER NOT NULL,
    valor FLOAT NOT NULL DEFAULT 0,
    ativo BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    profissional_id INTEGER NOT NULL,
    procedimento_id INTEGER NOT NULL,
    data VARCHAR(10) NOT NULL,
    horario VARCHAR(5) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Agendado',
    observacoes TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id),
    FOREIGN KEY (procedimento_id) REFERENCES procedimentos(id),
    CONSTRAINT uq_profissional_data_horario
        UNIQUE (profissional_id, data, horario)
);
