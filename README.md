# Taskmaster - Trab1 Web

Sistema web de gerenciamento de tarefas desenvolvido em Django para o Trabalho 1 da disciplina INF1407.

## Componentes do grupo

- Luiz Felipe Neves
- Matheus Nossar

## Relato do que foi desenvolvido

O projeto implementa um site chamado **Taskmaster**, voltado para organização pessoal de tarefas. A proposta é permitir que cada usuário mantenha suas próprias listas de tarefas, acompanhe prazos, organize prioridades e divida tarefas maiores em subtarefas.

O sistema foi desenvolvido com autenticação de usuários. Cada pessoa pode se cadastrar, entrar no site, sair da sessão e recuperar a senha. Depois do login, o usuário acessa um painel inicial com um resumo das suas tarefas e navega pelas listas cadastradas. Todos os dados são filtrados pelo usuário logado, impedindo que uma conta visualize, edite ou apague informações de outra.

### Funcionalidades implementadas

- Cadastro de usuário.
- Login e logout.
- Recuperação de senha por e-mail.
- Painel inicial com resumo das tarefas.
- Criação, visualização, edição e exclusão de listas.
- Criação, visualização, edição e exclusão de tarefas.
- Marcação de tarefas como concluídas.
- Criação, conclusão/desmarcação e exclusão de subtarefas.
- Organização de tarefas por lista.
- Cadastro de prioridade: baixa, média ou alta.
- Cadastro de status: pendente, em andamento ou concluída.
- Cadastro de data planejada e data de prazo.
- Exibição de tarefas vencidas, tarefas para hoje, tarefas concluídas na semana e próximas tarefas.

### Estrutura principal

- `users`: app responsável por cadastro, login, logout, recuperação de senha e painel inicial.
- `tasks`: app responsável por listas, tarefas e subtarefas.
- `templates`: páginas HTML do sistema.
- `static`: arquivos estáticos, incluindo a imagem do logo do Taskmaster.
- `trab1_web`: configuração principal do projeto Django.

## Funcionamento do site - manual do usuário

### 1. Entrar no sistema

Ao abrir o site, o usuário deve criar uma conta ou entrar com uma conta já existente.

Para criar uma conta:

1. Clique em **Cadastrar**.
2. Preencha os dados solicitados.
3. Envie o formulário.
4. Após o cadastro, o sistema faz login automaticamente e redireciona para o painel.

Para entrar com uma conta existente:

1. Clique em **Entrar**.
2. Informe usuário e senha.
3. Envie o formulário.

Para sair:

1. Clique em **Sair** no menu superior.

Para recuperar a senha:

1. Na tela de login, acesse a opção de recuperação de senha.
2. Informe o e-mail cadastrado.
3. Siga o link recebido por e-mail para definir uma nova senha.

Em ambiente de desenvolvimento, os e-mails de recuperação aparecem no terminal. Em produção, o envio usa o serviço Resend quando `DEBUG=False`.

### 2. Usar o painel inicial

Depois do login, a primeira tela é o **Painel**. Ele mostra um resumo geral das tarefas do usuário:

- **Pendentes**: quantidade de tarefas pendentes ou em andamento.
- **Vencidas**: tarefas ainda não concluídas cujo prazo já passou.
- **Para hoje**: tarefas planejadas para hoje ou com prazo para hoje.
- **Concluídas na semana**: tarefas marcadas como concluídas desde o início da semana.

O painel também mostra:

- **Minhas Listas**: cards com as listas do usuário e a quantidade de tarefas pendentes em cada uma.
- **Ações Rápidas**: atalhos para criar lista, iniciar criação de tarefa, ver atrasadas e ver concluídas.
- **Tarefas atrasadas**: tabela com tarefas vencidas.
- **Tarefas concluídas**: últimas tarefas finalizadas.
- **Próximas Tarefas**: tarefas urgentes, próximas do prazo ou de alta prioridade.

### 3. Criar uma lista

As tarefas sempre ficam dentro de uma lista. Exemplos de listas possíveis são "Faculdade", "Trabalho" ou "Pessoal".

Para criar uma lista:

1. Clique em **Ver listas** no menu superior ou em **Nova lista** no painel.
2. Clique em **Adicionar lista**.
3. Preencha:
  - **Name**: nome da lista.
  - **Description**: descrição opcional.
  - **Color**: cor da lista.
4. Clique em **Salvar**.

Depois de salvar, o sistema abre a página da lista criada.

### 4. Ver, editar ou apagar listas

Na página **Minhas listas**, cada lista aparece em um card.

Em cada card é possível:

- Clicar no nome da lista para abrir seus detalhes.
- Clicar em **Nova tarefa** para criar uma tarefa dentro daquela lista.
- Clicar em **Editar** para alterar nome, descrição ou cor.
- Clicar em **Apagar** para remover a lista.

Atenção: apagar uma lista também remove as tarefas e subtarefas associadas a ela.

### 5. Criar uma tarefa

Para criar uma tarefa:

1. Acesse **Ver listas**.
2. Escolha uma lista.
3. Clique em **Nova tarefa**.
4. Preencha os campos:
  - **Task list**: lista em que a tarefa ficará.
  - **Title**: título da tarefa.
  - **Description**: descrição opcional.
  - **Priority**: baixa, média ou alta.
  - **Status**: pendente, em andamento ou concluída.
  - **Due date**: prazo final.
  - **Planned date**: data planejada para executar a tarefa.
5. Clique em **Salvar**.

Após salvar, o sistema abre a página de detalhes da tarefa.

### 6. Acompanhar tarefas dentro de uma lista

Ao abrir uma lista, o usuário vê todas as tarefas daquele grupo. Cada tarefa mostra:

- Título.
- Descrição, se houver.
- Status.
- Prioridade.
- Data planejada.
- Prazo.

As tarefas aparecem ordenadas priorizando pendentes, depois em andamento e por último concluídas. Dentro dessa organização, o sistema também considera prazo, data planejada e título.

Na página da lista é possível:

- Abrir os detalhes de uma tarefa clicando no título.
- Editar a tarefa.
- Excluir a tarefa.
- Marcar a tarefa como concluída.

### 7. Editar, excluir ou concluir uma tarefa

Na página de detalhes de uma tarefa:

- Clique em **Editar** para alterar lista, título, descrição, prioridade, status, prazo ou data planejada.
- Clique em **Excluir** para apagar a tarefa.
- Clique em **Marcar como concluída** para mudar o status da tarefa para concluída.

Quando uma tarefa é concluída, ela passa a aparecer como **Concluída** e entra no resumo de tarefas finalizadas do painel.

### 8. Usar subtarefas

Subtarefas servem para quebrar uma tarefa maior em etapas menores.

Para adicionar uma subtarefa:

1. Abra a página de detalhes de uma tarefa.
2. Na seção **Subtarefas**, digite o nome da nova subtarefa.
3. Clique em **Adicionar**.

Para concluir uma subtarefa:

1. Clique em **Concluir** ao lado da subtarefa.

Para desmarcar uma subtarefa concluída:

1. Clique em **Desmarcar**.

Para excluir uma subtarefa:

1. Clique em **Excluir** ao lado da subtarefa.

As subtarefas concluídas aparecem riscadas, facilitando a visualização do progresso.

## Como rodar o projeto localmente

### 1. Instalar o uv

Se o `uv` ainda não estiver instalado:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Instalar as dependências

```bash
uv sync
```

Alternativa sem `uv`:

```bash
pip install .
```

### 3. Criar o arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com, no mínimo:

```env
SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=["localhost","127.0.0.1"]
DATABASE_URL=
```

O banco padrão em desenvolvimento é SQLite. Se `DATABASE_URL` for informado como vazio, o projeto usa `db.sqlite3`.

Para produção com envio real de e-mail, configure também:

```env
DEBUG=False
DATABASE_URL=postgres://usuario:senha@host:porta/banco
DEFAULT_FROM_EMAIL=noreply@example.com
RESEND_API_KEY=re_...
```

### 4. Aplicar as migrações

Com `uv`:

```bash
uv run manage.py migrate
```

Sem `uv`:

```bash
python manage.py migrate
```

### 5. Criar um superusuário, opcional

Use este passo apenas se quiser acessar o painel administrativo em `/admin/`.

Com `uv`:

```bash
uv run manage.py createsuperuser
```

Sem `uv`:

```bash
python manage.py createsuperuser
```

### 6. Rodar o servidor de desenvolvimento

Com `uv`:

```bash
uv run manage.py runserver
```

Sem `uv`:

```bash
python manage.py runserver
```

Depois acesse:

```text
http://127.0.0.1:8000/
```

## Rotas principais


| Rota                                       | Descrição                        |
| ------------------------------------------ | -------------------------------- |
| `/`                                        | Painel inicial do usuário logado |
| `/accounts/register/`                      | Cadastro                         |
| `/accounts/login/`                         | Login                            |
| `/accounts/logout/`                        | Logout                           |
| `/accounts/password-reset/`                | Recuperação de senha             |
| `/lists/`                                  | Listagem de listas               |
| `/lists/new/`                              | Criação de lista                 |
| `/lists/<id>/`                             | Detalhes de uma lista            |
| `/lists/<id>/edit/`                        | Edição de lista                  |
| `/lists/<id>/delete/`                      | Exclusão de lista                |
| `/lists/<list_id>/tasks/new/`              | Criação de tarefa                |
| `/lists/<list_id>/tasks/<task_id>/`        | Detalhes de tarefa               |
| `/lists/<list_id>/tasks/<task_id>/edit/`   | Edição de tarefa                 |
| `/lists/<list_id>/tasks/<task_id>/delete/` | Exclusão de tarefa               |


## Desenvolvimento

Instalar os hooks do pre-commit:

```bash
uv run pre-commit install
```

Rodar os testes:

```bash
uv run manage.py test
```
