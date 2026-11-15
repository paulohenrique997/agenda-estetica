# AgendaEstética — Entrega 2: Funcionalidades Básicas

Projeto acadêmico de sistema web para agendamento e gestão de atendimentos em clínicas de estética.

## Estrutura atual do repositório

Os arquivos da implementação estão reunidos na pasta `documentos`:

- `app.py`: aplicação Flask e endpoints da API.
- `templates/index.html`: página inicial carregada pelo Flask.
- `requirements.txt`: dependências Python.
- `schema.sql`: script DDL de criação das tabelas.
- `dados_iniciais.sql`: script DML com registros fictícios.
- `wireframes.html`: proposta visual das telas.
- `documentacao_api.md`: rotas, métodos HTTP e exemplos de requisições.
- `AgendaEstetica.postman_collection.json`: coleção para testes da API.

## Como executar

Requer Python 3.10 ou superior.

1. Abra um terminal na pasta `documentos`.
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o servidor:

   ```bash
   python app.py
   ```

4. Abra no navegador:

   ```
   http://127.0.0.1:5000/
   ```

Mantenha o terminal aberto enquanto utiliza o sistema. Não abra o arquivo HTML diretamente pelo explorador de arquivos; a página deve ser carregada pelo Flask.

## Banco de dados

A aplicação utiliza SQLite local, armazenado em `agenda_estetica.db`. O banco e as tabelas são criados automaticamente na primeira execução por meio de `db.create_all()`. Como esta versão usa SQLite local, não há host, porta ou credenciais de servidor remoto.

O arquivo `schema.sql` documenta a estrutura equivalente e `dados_iniciais.sql` contém registros fictícios. Para criar e popular um banco manualmente, execute primeiro o DDL e depois o DML em um banco vazio. Não execute os scripts sobre um banco que já contenha os mesmos registros.

## Endpoints implementados

- `GET /api/clientes` e `POST /api/clientes`.
- `GET /api/profissionais` e `POST /api/profissionais`.
- `GET /api/procedimentos` e `POST /api/procedimentos`.
- `GET /api/agendamentos` e `POST /api/agendamentos`.
- `PATCH /api/agendamentos/<id>`: atualiza data, horário ou status.
- `DELETE /api/agendamentos/<id>`: exclui um agendamento.

Nesta versão, atualização e exclusão estão disponíveis somente para agendamentos. Clientes, profissionais e procedimentos possuem listagem e cadastro.

## Interface e wireframes

A página inicial apresenta atalhos para consultar os endpoints. O arquivo `wireframes.html` é uma representação visual inicial das telas planejadas e não deve ser confundido com formulários já implementados na interface.

## Observações acadêmicas

Os dados de exemplo são fictícios. Não utilizar dados reais de pacientes ou clientes.
