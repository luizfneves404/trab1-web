# Pré-projeto — Todo List Avançado (Django)

## Visão Geral

Sistema web de gerenciamento de tarefas com autenticação por usuário.
Cada usuário terá acesso apenas aos próprios dados, podendo criar listas, tarefas e subtarefas.

---

# Funcionalidades Principais

- Cadastro de usuário
- Login
- Logout
- Recuperação de senha
- CRUD de listas
- CRUD de tarefas
- CRUD de subtarefas
- Prioridade de tarefas
- Datas de planejamento e entrega
- Dashboard inicial (homepage)
- Filtros e organização

---

# Models

## User (Django padrão)

- username
- email
- password

---

## TaskList

Representa grupos de tarefas.

- owner (User)
- name
- description
- created_at
- color

---

## Task

Tarefa principal do sistema.

- owner (User)
- task_list
- title
- description
- priority
- status
- due_date
- planned_date
- created_at
- updated_at

---

## SubTask

Etapas menores de uma tarefa.

- task
- title
- done

---

# Homepage (Dashboard)

A página inicial será um painel geral do usuário.

## Bloco 1 — Resumo Geral

Cards rápidos com:

- tarefas pendentes
- tarefas vencidas
- tarefas para hoje
- concluídas na semana

---

## Bloco 2 — Próximas Tarefas

Lista com tarefas mais urgentes:

- vencidas
- próximas do prazo
- alta prioridade

---

## Bloco 3 — Minhas Listas

Cards clicáveis:

- Faculdade
- Trabalho
- Pessoal

Cada card mostra quantidade de tarefas pendentes.

---

## Bloco 4 — Ações Rápidas

Botões:

- Nova tarefa
- Nova lista
- Ver atrasadas
- Ver concluídas

---

# Views

# Autenticação

## register_view

Cria nova conta de usuário.

## login_view

Realiza login no sistema.

## logout_view

Encerra sessão atual.

## password_reset_view

Solicita redefinição de senha por e-mail.

## password_reset_confirm_view

Permite cadastrar nova senha.

---

# Dashboard

## home_view

Exibe homepage com os 4 blocos principais.

---

# CRUD de Listas

## list_create

Cria nova lista.

## list_update

Edita lista existente.

## list_delete

Remove lista.

## list_detail

Mostra tarefas de uma lista específica.

---

# CRUD de Tarefas

## task_create

Cria tarefa.

## task_update

Edita tarefa.

## task_delete

Exclui tarefa.

## task_detail

Mostra detalhes completos.

## task_toggle_done

Marca como concluída ou pendente.

---

# CRUD de Subtarefas

## subtask_create

Adiciona subtarefa.

## subtask_toggle

Marca subtarefa como feita.

## subtask_delete

Remove subtarefa.

---

# Views Extras

## today_view

Mostra tarefas planejadas para hoje.

## late_tasks_view

Mostra tarefas vencidas.

## completed_view

Mostra tarefas concluídas.

## priority_view

Mostra tarefas ordenadas por prioridade.

---

# Gerência de Usuário

- Todo objeto pertence a um usuário.
- Usuário não acessa dados de outro.
- Edição e exclusão apenas dos próprios dados.
- Queries sempre filtradas por `request.user`.

Exemplo:

```python
Task.objects.filter(owner=request.user)
