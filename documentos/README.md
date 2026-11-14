# AgendaEstética — Entrega 2: Funcionalidades Básicas

Projeto acadêmico de sistema web para agendamento e gestão de atendimentos em clínicas de estética.

## Conteúdo
- `database/schema.sql`: script DDL para criação das tabelas.
- `database/dados_iniciais.sql`: script DML com registros fictícios para testes.
- `backend/app.py`: aplicação Flask com API REST inicial e persistência SQLite via SQLAlchemy.
- `backend/requirements.txt`: dependências necessárias.
- `backend/templates/index.html`: interface inicial navegável.
- `wireframes/wireframes.html`: wireframe visual das principais telas.

## Requisitos
- Python 3.10 ou superior.

## Como executar
1. Abra a pasta `backend` no terminal.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute:
   ```bash
   python app.py
   ```
4. Acesse `http://127.0.0.1:5000`.

O banco `agenda_estetica.db` será criado automaticamente na primeira execução. O SQLite é utilizado localmente nesta versão inicial; por isso, não há host, porta ou credenciais de banco remoto.

## Endpoints iniciais
- `GET /api/clientes` — lista clientes.
- `POST /api/clientes` — cadastra cliente.
- `GET /api/profissionais` — lista profissionais.
- `POST /api/profissionais` — cadastra profissional.
- `GET /api/procedimentos` — lista procedimentos.
- `POST /api/procedimentos` — cadastra procedimento.
- `GET /api/agendamentos` — lista agendamentos.
- `POST /api/agendamentos` — cadastra agendamento.
- `PATCH /api/agendamentos/<id>` — atualiza status, data ou horário.
- `DELETE /api/agendamentos/<id>` — exclui um agendamento de teste.

## Observações acadêmicas
Os dados incluídos são fictícios. Esta é uma versão inicial para a Entrega 2 e deverá ser testada, revisada e ampliada conforme a orientação do professor. Não utilizar dados reais de pacientes/clientes.
