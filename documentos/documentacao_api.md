# Documentação da API — AgendaEstética

## Visão geral
API desenvolvida em Python com Flask e Flask-SQLAlchemy, utilizando banco SQLite local.

## Execução
A partir da pasta que contém `app.py` e a pasta `templates`:

```bash
pip install -r requirements.txt
python app.py
```

A aplicação fica disponível em `http://127.0.0.1:5000`. O arquivo do banco de dados é criado localmente como `agenda_estetica.db`.

## Endpoints implementados

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/clientes` | Lista clientes |
| POST | `/api/clientes` | Cadastra cliente |
| GET | `/api/profissionais` | Lista profissionais |
| POST | `/api/profissionais` | Cadastra profissional |
| GET | `/api/procedimentos` | Lista procedimentos |
| POST | `/api/procedimentos` | Cadastra procedimento |
| GET | `/api/agendamentos` | Lista agendamentos |
| POST | `/api/agendamentos` | Cadastra agendamento |
| PATCH | `/api/agendamentos/<id>` | Atualiza data, horário ou status |
| DELETE | `/api/agendamentos/<id>` | Exclui agendamento |

A versão atual oferece listagem e cadastro para clientes, profissionais e procedimentos. Atualização e exclusão estão disponíveis somente para agendamentos.

## Exemplos JSON

### POST /api/clientes
```json
{
  "nome": "Mariana Costa",
  "telefone": "(49) 99999-0001",
  "email": "mariana.teste@example.com"
}
```

### POST /api/profissionais
```json
{
  "nome": "Carla Souza",
  "especialidade": "Estética facial",
  "telefone": "(49) 99999-1001"
}
```

### POST /api/procedimentos
```json
{
  "nome": "Limpeza de pele",
  "descricao": "Procedimento demonstrativo",
  "duracao_minutos": 60,
  "valor": 150.0
}
```

### POST /api/agendamentos
Os IDs devem existir previamente no banco.
```json
{
  "cliente_id": 1,
  "profissional_id": 1,
  "procedimento_id": 1,
  "data": "2026-11-20",
  "horario": "14:00",
  "observacoes": "Agendamento de teste"
}
```

### PATCH /api/agendamentos/1
```json
{
  "status": "Concluído"
}
```

Status previstos: `Agendado`, `Concluído` e `Cancelado`.

## Respostas HTTP
- 200: consulta ou atualização realizada.
- 201: registro criado.
- 400: dados ausentes ou inválidos.
- 404: registro relacionado ou agendamento não encontrado.
- 409: conflito, como e-mail duplicado ou horário já ocupado.

Erros retornam JSON com os campos `sucesso` e `mensagem`.

## Banco de dados
A aplicação usa SQLite local. A criação automática das tabelas ocorre por `db.create_all()` na inicialização do Flask. Os scripts SQL no repositório são materiais de documentação e preparação do banco; compare-os com os modelos Python antes de executar ambos no mesmo banco.