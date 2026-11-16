# Capítulo 4 — Prompts para Codex/Copilot

## Prompt 1 — Testes do serviço

- **Contexto:** Tenho TaskService com CRUD de tarefas.

- **Objetivo:** Gerar uma suíte Pytest que cubra criação, listagem, atualização, exclusão e o erro
  por ID inexistente.

- **Estilo:** Testes claros, nomes descritivos e fixtures simples.

- **Resposta:** Crie o código completo em tests/test_task_service.py

## Prompt 2 — Teste do PriorityAdvisor

- **Contexto:** PriorityAdvisor possui heurística local e fallback quando a chamada externa falha.

- **Objetivo:** Gerar testes para os três níveis de prioridade e para o fallback.

- **Estilo:** Use `monkeypatch` quando necessário.

- **Resposta:** Crie o arquivo completo em `tests/test_priority_advisor.py`.

## Prompt 3 — Testes de API

- **Contexto:** API FastAPI com endpoints CRUD em `/tasks`.

- **Objetivo:** Criar testes de rota com `TestClient` para os status 201, 200, 204 e 404.

- **Estilo:** Isolar dependência de repositório para evitar estado global entre testes.

- **Resposta:** Crie o arquivo completo em `tests/test_task_routes.py`.

## Prompt 4 — Refatoração de DRY/SRP

- **Contexto:** Analise os arquivos app/services/task_service.py e
  app/repositories/task_repository.py

- **Objetivo:** Sugerir refatoração com foco em DRY e SRP sem mudar comportamento externo.

- **Resposta:** Apresente (1) uma lista de mudanças propostas e (2) um patch sugerido para cada arquivo.

## Prompt 5 — README final técnico

- **Contexto:** MVP de micro-API de tarefas com prioridade assistida por IA.

- **Objetivo:** Gerar um README completo com instalação, execução, testes, arquitetura, exemplos de
  uso, limitações e próximos passos.
- **Estilo:** Use Markdown profissional e objetivo.

- **Resposta:** Gere o README completo.

## Prompt 6 — Revisão final de qualidade

- **Contexto:** Com base no código e nos testes atuais, gere um checklist com: I) Riscos técnicos
  restantes; II) Gaps de cobertura de testes; III) Melhorias prioritárias para a próxima release.

- **Resposta:** use bullets curtos.

#### I. Riscos técnicos restantes

- Sem autenticação/autorização: não exponha a API a uma rede compartilhada ou pública sem proteção.

- SQLite sem migrações, backup ou controle de concorrência: update lê e grava em conexões separadas,
  permitindo atualizações concorrentes conflitantes.

- Modelo limitado: tarefas não têm status, prazo nem prioridade persistida; a sugestão de prioridade
  não tem endpoint HTTP.

- Gasto de LLM sem cota: com chave configurada, cada sugestão pode chamar a API; não há limite de
  uso ou orçamento.

- Erros sem formato comum: a API ainda usa respostas padrão do FastAPI.

#### II. Gaps de cobertura de testes

- Falta teste da rota /health.

- Faltam cenários de rollback e atualização concorrente do SQLite.

- Faltam testes de advisor para timeout e resposta LLM inválida ou malformada.

- Falta verificar que uma sugestão de prioridade não altera a tarefa.

- Confirme que `tests/test_priority_advisor.py` faz parte da suíte executada. O Pytest normalmente
  o encontra pela descoberta padrão; o comando documentado também pode listá-lo explicitamente.

#### III. Melhorias prioritárias para a próxima release

- Implementar autenticação e autorização antes do uso pela equipe.

- Expandir o modelo e as rotas para status, prazo e prioridade; adicionar endpoint de sugestão sem
  persistência automática.

- Configurar caminho do banco, migrações, backup e controle de concorrência.

- Definir cotas e orçamento para chamadas LLM, mantendo a heurística local como fallback.

- Completar os cenários de teste indicados, padronizar a descoberta Pytest e executá-la no CI.

## Prompt 7 — Commits das alterações realizadas

- **Contexto:** Execute `git status` e `git diff` para inspecionar as alterações pendentes no
  workspace.

- **Objetivo:** Analisar os diffs e dividir as alterações em commits atômicos usando Conventional
  Commits.

- **Resposta:** Execute os comandos git correspondentes.
