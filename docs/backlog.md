# Backlog mínimo do MVP — Micro-API de Gestão de Tarefas

Referência: [escopo-mvp.md](escopo-mvp.md), incluindo contrato e riscos das seções 8 e 9. RF identifica requisito funcional; RT identifica trabalho técnico e referencia os RNF existentes. Todos os itens aguardam validação de aceite; caixas desmarcadas não afirmam ausência de implementação.

## Release 1 — Core

- [ ] **RT-01 — Decisões técnicas antes da implementação** (RNF-01, RNF-03, RNF-05)
  - [ ] Registrar banco escolhido, migração inicial, carga concorrente prevista e estratégia de transação/versão.
  - [ ] Definir autenticação, autorização e fronteira de rede antes do uso compartilhado.
  - [ ] Documentar execução, dependências e configuração sem segredos versionados.

- [ ] **RT-02 — Estrutura e isolamento de testes** (RNF-05, RNF-08)
  - [ ] Separar API, Service e Repository; permitir injetar Repository, relógio e PriorityAdvisor.
  - [ ] Criar fixtures com banco temporário por teste e dados determinísticos.
  - [ ] Documentar comando único para executar a suíte sem rede ou dados reais.

- [ ] **RF-01 — Saúde** (RNF-04)
  - [ ] GET /health retorna 200, status ok e timestamp ISO 8601 com fuso.
  - [ ] Relógio simulado produz timestamp previsível no teste.

- [ ] **RT-03 — Persistência transacional** (RNF-03)
  - [ ] Migração inicial cria o modelo definido no escopo.
  - [ ] Dados continuam disponíveis após fechar e reabrir o banco.
  - [ ] Falha de escrita causa rollback sem alteração parcial.
  - [ ] Duas atualizações com a mesma versão permitem somente uma escrita; a outra retorna 409.

- [ ] **RF-02 — Criar tarefa** (RF-06, RNF-02)
  - [ ] POST /tasks retorna 201 com UUID, versão 1 e timestamps em UTC.
  - [ ] Aplicar padrões: status pendente, prioridade media, descrição e prazo nulos.
  - [ ] Aceitar título normalizado de 1 a 200 caracteres e descrição até 2.000.
  - [ ] Título vazio, excesso de tamanho, nulos proibidos, campos desconhecidos e prazo sem fuso retornam 422.

- [ ] **RF-03 — Consultar e listar tarefas: parte core** (RNF-06)
  - [ ] GET /tasks/{id} retorna 200; UUID inexistente retorna 404; formato inválido retorna 422.
  - [ ] GET /tasks usa limit padrão 20, intervalo de 1 a 100 e ID crescente.
  - [ ] Banco vazio retorna 200 com lista vazia; limit inválido retorna 422.
  - [ ] Filtros, ordenação configurável e offset ficam para a release 2.

- [ ] **RF-04 — Atualizar tarefa** (RF-06, RF-08, RNF-02)
  - [ ] PATCH preserva campos omitidos e limpa somente descrição/prazo quando recebem nulo.
  - [ ] expected_version é obrigatório; versão obsoleta retorna 409 sem escrita; registro inexistente retorna 404.
  - [ ] Aplicar transições da seção 8 do escopo; transição proibida retorna 409.
  - [ ] Atualização válida retorna 200 e incrementa versão; ID e created_at permanecem iguais.
  - [ ] Payload sem campo editável ou contendo ID/timestamps retorna 422.

- [ ] **RF-05 — Excluir tarefa** (RNF-02)
  - [ ] DELETE com expected_version atual retorna 204 sem corpo e remove o registro.
  - [ ] Registro inexistente retorna 404; versão obsoleta retorna 409 sem excluir.
  - [ ] Ausência ou formato inválido de expected_version retorna 422.

- [ ] **RT-04 — Contrato, proteção e testes básicos** (RF-09, RNF-01, RNF-02, RNF-07, RNF-08)
  - [ ] OpenAPI descreve rotas entregues, schemas, parâmetros e respostas.
  - [ ] Erros seguem detail com code/message; respostas não expõem segredos ou stack traces.
  - [ ] Validar 401 sem credencial válida e 403 sem permissão em rotas protegidas.
  - [ ] Testes cobrem saúde, CRUD, limites, nulos, transições, persistência e concorrência.
  - [ ] Testes passam antes de encerrar o core e não chamam provedor externo.

## Release 2 — Qualidade

- [ ] **RF-03 — Filtros, ordenação e paginação: complemento** (RNF-06)
  - [ ] Adicionar offset inteiro ≥ 0, padrão 0, mantendo limit de 1 a 100.
  - [ ] Filtrar por status e ordenar por prazo ou prioridade com direction asc/desc.
  - [ ] Aplicar desempate por ID crescente, prazo nulo por último e sequência de prioridade do escopo.
  - [ ] Cobrir combinações, páginas vazias, empate e parâmetros inválidos com testes.

- [ ] **RT-05 — Regressão e observabilidade** (RNF-02, RNF-04, RNF-08)
  - [ ] Ampliar a suíte para filtros, ordenação e falhas de dependências.
  - [ ] Logs registram operação, resultado e erros sem credenciais ou payload sensível.
  - [ ] Automatizar a execução da suíte no fluxo de integração do projeto.

- [ ] **RT-06 — Decisão sobre IA antes do adapter** (RF-07, RNF-01, RNF-08)
  - [ ] Registrar provedor/modelo, dados permitidos, tokens por chamada e orçamento por período.
  - [ ] Definir cota de chamadas que limite o gasto ao orçamento e bloqueio ao esgotá-la.
  - [ ] Se as decisões não estiverem concluídas, registrar adiamento e manter IA desabilitada.

- [ ] **RF-07 — Sugestão opcional de prioridade** (RNF-08; depende de RT-06)
  - [ ] Aplicar timeout total de 5 segundos, sem repetição automática.
  - [ ] Validar prioridade enumerada e justificativa de 1 a 300 caracteres.
  - [ ] Enviar somente campos permitidos; respeitar tokens e cota configurados.
  - [ ] Retornar 503 quando desabilitada, 504 em timeout e 502 em resposta inválida.
  - [ ] Simular sucesso, timeout, resposta inválida e cota esgotada; tarefa permanece igual e CRUD operacional.

- [ ] **RF-08 — Aplicação manual da sugestão**
  - [ ] Quando IA estiver habilitada, aplicar ou ajustar a sugestão via PATCH com expected_version.
  - [ ] Somente a atualização explícita persiste a prioridade; sugestão isolada não altera versão nem tarefa.

- [ ] **RF-09 — Completar documentação OpenAPI** (RNF-07)
  - [ ] Publicar exemplos de paginação, erros, concorrência e IA quando habilitada.
  - [ ] Documentar configuração, limites e dados enviados ao provedor.

## Release 3 — Entrega final

- [ ] **RT-07 — Homologação de acesso e capacidade** (RNF-01, RNF-03, RNF-06)
  - [ ] Confirmar controles implementados no core, inclusive documentação e IA quando habilitada.
  - [ ] Verificar a carga interna prevista em RT-01 e registrar limites observados.
  - [ ] Se SQLite for adotado, verificar bloqueios e escritas simultâneas nessa carga.

- [ ] **RT-08 — Operação e recuperação** (RNF-03, RNF-05)
  - [ ] Outra pessoa prepara e inicia o serviço seguindo a documentação.
  - [ ] Documentar migrações, configuração e procedimento de backup consistente.
  - [ ] Restaurar uma cópia em banco isolado e conferir tarefas recuperadas.

- [ ] **RT-09 — Aceite final** (RF-01 a RF-09, RNF-01 a RNF-08)
  - [ ] Reexecutar regressão e conferir critérios de conclusão do escopo.
  - [ ] Registrar evidências, limitações e estado habilitado/desabilitado da IA.
  - [ ] Se IA for adiada, marcar RF-07 e a parte assistida de RF-08 como adiadas, mantendo prioridade manual disponível.

## Dependências e conclusão

- RT-01 precede implementação de persistência e acesso; RT-02 prepara testes desde o core.
- RT-03 precede RF-02 a RF-05; RT-04 encerra a release inicial.
- RT-06 precede RF-07; RF-08 assistido depende de RF-07 e RF-04.
- RF-06 é coberto pelo modelo, criação e atualização; RF-03 é concluído na release 2.
- Toda entrega deve incluir critérios de aceite verificados e contrato atualizado; segurança e testes básicos são exigidos desde o core.
