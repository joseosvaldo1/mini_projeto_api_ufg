## Capítulo 4 - Prompts para Codex/Copilot:

# Prompt 1 - Testes do service:
Contexto: Tenho TaskService com CRUD de tarefas.
Objetivo: Gerar suite Pytest cobrindo criação, listagem, atualização,
exclusão e caso de erro por ID inexistente.
Estilo: Testes claros, nomes descritivos e fistures simples.
Resposta: Crie o código completo em tests/test_task_serice.py

# Prompt 2 - teste do PriorityAdvisor:
Contexto: PriorityAdvisor possui heuristica local e fallback quando a
chamada externa falha.
Objetivo: Gerar testes para os tres niveis de prioridade e para fallback
Estilo: Usar monkeypatch quando necessario.
Resposta: Crie o código completo em tests/teste_priority_advisor.py

# Prompt 3 - Testes de API
Contexto: API FastAPI com endpoints CRUD de /tasks.
Objetivo: Criar testes de rota com TestClient para status 201, 200, 204
e 404.
Estilo: Isolar dependência de repositório para evitar estado global entre
testes.
Resposta: Crie o código comple em tests/test_task_routes.py

# Prompt 4 - Refatoração de DRY/SRP:
Contexto: Analise os arquivos app/services/task_service.py e
app/repositories/task_repository.py
Objetivo: Sugerir refatoração com foco em DRY e SRP sem mudar
comportamento externo.
Resposta: 1) lista de mudanças propostas; 2) patch sugerido por arquivo.

# Prompt 5 - README final técnico:
Contexto: MVP de micro-API de tarefas com prioridade assistida por IA.
Objetivo: Gerar README completo com instalação, execução, testes,
arquitetura, usos, limitações e próximos passos.
Estilo Markdown profissional e objetivo.
Resposta: README inteiro.

# Prompt 6 - Revisão final de qualidade:
Contexto: Com base no código e nos testes atuais, gere um checklist com:
I) Riscos técnicos restantes;
II) Gaps de cobertura de testes;
III) Melhorias prioritárias para a próxima release.
Resposta: em bullets curtos.


I) Riscos técnicos restantes

- Sem autenticação/autorização: não exponha a API a uma rede compartilhada
ou pública sem proteção.
- SQLite sem migrações, backup ou controle de concorrência: update lê e
grava em conexões separadas, permitindo atualizações concorrentes conflitantes.
- Modelo limitado: tarefas não têm status, prazo nem prioridade persistida;
a sugestão de prioridade não tem endpoint HTTP.
- Gasto de LLM sem cota: com chave configurada, cada sugestão pode chamar a
API; não há limite de uso ou orçamento.
- Erros sem formato comum: a API ainda usa respostas padrão do FastAPI.

II) Gaps de cobertura de testes

- Falta teste da rota /health.
- Faltam cenários de rollback e atualização concorrente do SQLite.
- Faltam testes de advisor para timeout e resposta LLM inválida ou malformada.
- Falta verificar que uma sugestão de prioridade não altera a tarefa.
- teste_priority_advisor.py pode não ser encontrado pela descoberta padrão do
Pytest; o README precisa listá-lo explicitamente.

III) Melhorias prioritárias para a próxima release

- Implementar autenticação e autorização antes do uso pela equipe.
- Expandir o modelo e as rotas para status, prazo e prioridade; adicionar
endpoint de sugestão sem persistência automática.
- Configurar caminho do banco, migrações, backup e controle de concorrência.
- Definir cotas e orçamento para chamadas LLM, mantendo a heurística local
como fallback.
- Completar os cenários de teste indicados, padronizar a descoberta Pytest
e executá-la no CI.

# Prompt 7 - Commits das alterações realizadas:
Contexto: Execute `git status` e `git diff` para inspecionar as
alterações pendentes no workspace.
Objetivo: Analisar os diffs e dividir as alterações em commits atômicos
usando Conventional Commits.
Resposta: Execute os comandos git correspondentes.
