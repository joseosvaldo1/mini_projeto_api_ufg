# Backlog mínimo do MVP — Micro-API de Gestão de Tarefas

## Release 1 — Core

### [ ] CORE-01 — Estrutura inicial e configuração
- **Requisitos:** RNF-05, RNF-07
- **Descrição:** criar a aplicação FastAPI, declarar dependências, separar configuração por ambiente e disponibilizar o comando de execução local.
- **Critérios de aceite:**
  - [ ] A aplicação inicia com o comando documentado.
  - [ ] A instância FastAPI está disponível para o servidor ASGI.
  - [ ] Dependências e configurações estão declaradas no repositório.

### [ ] CORE-02 — Rota de saúde
- **Requisitos:** RF-01, RNF-04
- **Descrição:** implementar endpoint de verificação de saúde.
- **Critérios de aceite:**
  - [ ] Requisição válida retorna HTTP 200.
  - [ ] A resposta informa `status: "ok"`.
  - [ ] A resposta contém timestamp ISO 8601 com fuso horário.

### [ ] CORE-03 — Modelo e persistência de tarefas
- **Requisitos:** RF-02, RF-06, RNF-03
- **Descrição:** criar modelo e persistência durável com identificador, título, descrição, status, prioridade, prazo e timestamps.
- **Critérios de aceite:**
  - [ ] Toda tarefa recebe identificador único.
  - [ ] Status e prioridade aceitam apenas valores documentados.
  - [ ] Dados sobrevivem ao reinício do processo.

### [ ] CORE-04 — Criar tarefa
- **Requisitos:** RF-02, RNF-02
- **Descrição:** implementar endpoint de cadastro.
- **Critérios de aceite:**
  - [ ] Título é obrigatório e validado.
  - [ ] Campos opcionais têm valores padrão documentados.
  - [ ] Resposta retorna a tarefa criada.
  - [ ] Entrada inválida retorna erro HTTP consistente.

### [ ] CORE-05 — Listar e consultar tarefas
- **Requisitos:** RF-03, RNF-06
- **Descrição:** implementar listagem, consulta por identificador, filtro por status e ordenação por prazo ou prioridade.
- **Critérios de aceite:**
  - [ ] Listagem retorna tarefas persistidas.
  - [ ] Filtro e ordenação funcionam conforme parâmetros.
  - [ ] Existe paginação ou limite máximo documentado.
  - [ ] Identificador inexistente retorna HTTP 404.

### [ ] CORE-06 — Atualizar e excluir tarefa
- **Requisitos:** RF-04, RF-05, RF-08, RNF-02
- **Descrição:** implementar atualização e exclusão por identificador.
- **Critérios de aceite:**
  - [ ] Campos recebidos são validados.
  - [ ] Identificador e timestamp de criação não mudam.
  - [ ] Prioridade pode ser ajustada manualmente.
  - [ ] Exclusão remove a tarefa e retorna sucesso documentado.
  - [ ] Identificador inexistente retorna HTTP 404.

## Release 2 — Qualidade

### [ ] QUAL-01 — Contrato e documentação OpenAPI
- **Requisitos:** RF-09, RNF-07
- **Descrição:** completar documentação de endpoints, modelos, parâmetros, respostas e exemplos.
- **Critérios de aceite:**
  - [ ] Todas as rotas do MVP aparecem no OpenAPI.
  - [ ] Campos obrigatórios, enums e erros estão descritos.
  - [ ] Há exemplos dos fluxos principais.

### [ ] QUAL-02 — Padronização de erros e validações
- **Requisitos:** RNF-02, RNF-07
- **Descrição:** consolidar formato de erros e validações de limites, datas e enums.
- **Critérios de aceite:**
  - [ ] Erros usam formato consistente.
  - [ ] Respostas não expõem stack trace ou segredo.
  - [ ] Payloads incompletos e valores inválidos são rejeitados.

### [ ] QUAL-03 — Testes automatizados do núcleo
- **Requisitos:** RNF-08
- **Descrição:** cobrir saúde, CRUD, filtros, ordenação, persistência e falhas esperadas.
- **Critérios de aceite:**
  - [ ] Há testes para os fluxos CRUD.
  - [ ] Há testes para entradas inválidas e IDs inexistentes.
  - [ ] A suíte executa por comando documentado.
  - [ ] Testes não dependem de serviço externo de IA.

### [ ] QUAL-04 — Observabilidade e configuração segura
- **Requisitos:** RNF-01, RNF-04, RNF-05
- **Descrição:** configurar logs operacionais, tratamento seguro de falhas e parâmetros por ambiente.
- **Critérios de aceite:**
  - [ ] Eventos essenciais são registrados para diagnóstico.
  - [ ] Credenciais e dados sensíveis não aparecem nos logs.
  - [ ] Segredos vêm de configuração externa.

### [ ] QUAL-05 — Sugestão opcional de prioridade por IA
- **Requisitos:** RF-07, RF-08, RNF-08
- **Descrição:** integrar provedor configurável para sugerir prioridade e justificativa sem bloquear o CRUD.
- **Critérios de aceite:**
  - [ ] Provedor configurado retorna sugestão e justificativa curta.
  - [ ] Sugestão não altera automaticamente a prioridade persistida.
  - [ ] Prioridade final pode ser aplicada ou ajustada manualmente.
  - [ ] Falha ou ausência do provedor não interrompe operações básicas.
  - [ ] Provedor pode ser substituído por simulação nos testes.

## Release 3 — Entrega final

### [ ] ENT-01 — Revisão de segurança e acesso interno
- **Requisitos:** RNF-01
- **Descrição:** validar execução em ambiente restrito e documentar acesso autorizado.
- **Critérios de aceite:**
  - [ ] Ambiente e rede de acesso estão documentados.
  - [ ] Exposição pública não é pressuposta sem autenticação e autorização.
  - [ ] Segredos e permissões foram revisados.

### [ ] ENT-02 — Empacotamento e instruções de execução
- **Requisitos:** RNF-03, RNF-05, RNF-07
- **Descrição:** consolidar instalação, configuração, inicialização, persistência e operação.
- **Critérios de aceite:**
  - [ ] Uma pessoa da equipe prepara o ambiente seguindo a documentação.
  - [ ] Comando de inicialização e URL da documentação estão informados.
  - [ ] Persistência e cópia de segurança estão descritas.

### [ ] ENT-03 — Verificação final do MVP
- **Requisitos:** RF-01 a RF-09, RNF-01 a RNF-08
- **Descrição:** executar regressão e confirmar conclusão do escopo.
- **Critérios de aceite:**
  - [ ] Saúde e CRUD funcionam com dados persistidos.
  - [ ] Filtros, ordenação, status, prioridade e validações funcionam.
  - [ ] Respostas de sucesso e erro estão documentadas.
  - [ ] IA respeita confirmação manual quando habilitada.
  - [ ] Limitações e fora de escopo estão registrados.

## Dependências e ordem sugerida

- [ ] `CORE-01` precede os demais itens.
- [ ] `CORE-03` precede `CORE-04`, `CORE-05` e `CORE-06`.
- [ ] `QUAL-01` deve ser finalizado antes de `ENT-03`.
- [ ] `QUAL-03` depende das rotas do core.
- [ ] `QUAL-05` é opcional para o CRUD; se IA fizer parte da entrega, deve preceder `ENT-03`.
- [ ] `ENT-01` e `ENT-02` devem preceder a entrega à equipe interna.
