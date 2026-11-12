# Escopo do MVP — Micro-API de Gestão de Tarefas

## 1. Objetivo

Disponibilizar uma API HTTP de uso interno para centralizar o cadastro e o acompanhamento de tarefas da equipe. O MVP deve permitir operações básicas de gestão, consulta e priorização, com persistência dos dados e documentação dos endpoints. Quando habilitada, a integração com IA poderá sugerir prioridades; a decisão final permanece com a pessoa usuária.

## 2. Público e contexto de uso

- **Público:** integrantes e sistemas autorizados da equipe interna.
- **Forma de acesso:** chamadas HTTP/JSON, com contrato documentado via OpenAPI.
- **Contexto:** serviço interno, sem interface gráfica própria.
- **Premissa:** a API não deve ser exposta publicamente sem mecanismo de autenticação e autorização definido e implementado.

## 3. Requisitos funcionais

### RF-01 — Verificação de saúde

A API deve disponibilizar uma rota de saúde que informe o estado do serviço e um timestamp em formato ISO 8601 com fuso horário.

### RF-02 — Criar tarefa

A API deve permitir criar uma tarefa com, no mínimo, título e, opcionalmente, descrição, status, prazo e prioridade. Na criação, deve atribuir identificador único e valores padrão documentados para campos opcionais aplicáveis.

### RF-03 — Listar e consultar tarefas

A API deve permitir listar tarefas e consultar uma tarefa pelo identificador. A listagem deve aceitar filtros por status e ordenação por prazo ou prioridade. Respostas devem ser pagináveis ou possuir limite máximo documentado para evitar retornos sem controle de volume.

### RF-04 — Atualizar tarefa

A API deve permitir atualizar os campos editáveis de uma tarefa existente, validando os dados recebidos. A atualização não deve alterar o identificador nem os timestamps de criação.

### RF-05 — Excluir tarefa

A API deve permitir excluir uma tarefa pelo identificador e retornar resposta adequada quando o registro não existir.

### RF-06 — Status e prioridade

A API deve representar status e prioridade por valores enumerados e documentados. Os valores iniciais devem cobrir tarefas pendentes, em andamento e concluídas, e níveis de prioridade baixa, média e alta. Transições inválidas devem ser rejeitadas.

### RF-07 — Sugestão assistida de prioridade

Quando a integração de IA estiver configurada, a API deve permitir solicitar uma sugestão de prioridade para uma tarefa e retornar uma justificativa curta. A sugestão não deve alterar automaticamente a prioridade persistida. Indisponibilidade ou falta de credenciais do provedor não deve impedir as operações básicas de tarefas.

### RF-08 — Aceitar ou ajustar sugestão

A pessoa usuária deve poder aplicar manualmente a prioridade sugerida ou informar outra prioridade por meio da atualização normal da tarefa. A API deve manter a prioridade final escolhida pela pessoa usuária.

### RF-09 — Documentação da API

A API deve publicar contrato OpenAPI atualizado com rotas, modelos, parâmetros, códigos de resposta e exemplos de uso.

## 4. Requisitos não funcionais

### RNF-01 — Segurança de acesso

O serviço deve ser executado em rede ou ambiente restrito à equipe autorizada. Antes do primeiro uso compartilhado, deve haver autenticação e autorização compatíveis com a política interna, mesmo em rede interna. Segredos e credenciais não devem ser versionados nem registrados em logs.

### RNF-02 — Validação e consistência

Entradas devem ser validadas na fronteira da API. Respostas de erro devem usar códigos HTTP apropriados e formato consistente, sem expor stack traces, segredos ou detalhes internos.

### RNF-03 — Persistência

Tarefas devem sobreviver à reinicialização do processo. O mecanismo de persistência e a estratégia de cópia de segurança devem ser documentados para o ambiente de execução escolhido.

### RNF-04 — Observabilidade

O serviço deve registrar eventos operacionais e erros com informação suficiente para diagnóstico, sem incluir credenciais ou conteúdo sensível desnecessário. A rota de saúde deve permitir verificação automatizada de disponibilidade.

### RNF-05 — Manutenibilidade

A implementação deve manter separação entre rotas, validação, regras de negócio e persistência, com dependências e configuração declaradas. A configuração por ambiente deve permitir executar o serviço sem inserir segredos no código-fonte.

### RNF-06 — Desempenho e limites

Para o volume esperado de uso interno, as operações CRUD devem responder sem processamento em lote ou tarefas em segundo plano. A listagem deve impor paginação ou limite documentado. Metas numéricas de latência e capacidade serão definidas após conhecer a carga esperada.

### RNF-07 — Compatibilidade e contrato

A API deve usar HTTP e JSON, manter formatos de data e hora com fuso explícito e documentar mudanças incompatíveis no contrato.

### RNF-08 — Testabilidade

Regras principais, validações, respostas de erro e integração opcional de IA devem poder ser verificadas em testes automatizados, com o provedor de IA substituível por um componente simulado.

## 5. Fora de escopo

- Interface web, aplicativo móvel ou experiência de usuário além da documentação OpenAPI.
- Autenticação corporativa avançada, federação de identidade e gestão de permissões por função, até que a política interna seja definida.
- Exposição pública ou multiempresa/multitenant.
- Atribuição de tarefas a usuários, equipes ou grupos.
- Comentários, anexos, etiquetas, subtarefas, dependências, recorrência e histórico detalhado de auditoria.
- Notificações por e-mail, chat, push ou lembretes automáticos.
- Fluxos de aprovação, automações e regras configuráveis de negócio.
- Relatórios analíticos, painéis e exportações avançadas.
- Garantias de disponibilidade, escala horizontal, recuperação de desastre ou metas de SLA de produção.
- A IA tomar decisões, alterar prioridades sem confirmação ou garantir a correção das recomendações.

## 6. Critérios de conclusão do MVP

O MVP será considerado concluído quando:

1. As rotas de saúde e de operações CRUD estiverem implementadas e descritas no OpenAPI.
2. For possível criar, listar, consultar, atualizar e excluir tarefas persistidas.
3. Filtros, ordenação, status, prioridade e validações estiverem documentados e funcionais.
4. Erros para entradas inválidas e identificadores inexistentes tiverem respostas HTTP consistentes.
5. A integração de IA, se habilitada, retornar sugestão e justificativa sem sobrescrever a prioridade definida pela pessoa usuária; sem configuração do provedor, o CRUD continuará operacional.
6. As limitações de acesso e a configuração necessária para execução no ambiente interno estiverem documentadas.

## 7. Entrega incremental

- **Release 1 — Core:** saúde, CRUD persistido, listagem limitada, prioridade manual, contrato mínimo, acesso protegido e testes básicos.
- **Release 2 — Qualidade:** filtros, ordenação, paginação com offset, regressão ampliada e integração opcional de IA.
- **Release 3 — Entrega final:** homologação interna, instruções operacionais, restauração de backup e revisão dos critérios de aceite.

## 8. Contrato mínimo para implementação e testes

As decisões abaixo são a referência para os critérios de aceite e completam RF-01 a RF-09.

| Campo ou operação | Regra |
| --- | --- |
| Identificador | UUID gerado pelo servidor; formato inválido retorna 422. |
| Título | Texto com 1 a 200 caracteres após remover espaços nas extremidades; obrigatório e não nulo. |
| Descrição | Texto opcional de até 2.000 caracteres; padrão nulo. |
| Status | Valores pendente, em_andamento e concluida; padrão pendente. |
| Transições | pendente → em_andamento; em_andamento → pendente ou concluida; concluida → em_andamento. Repetir o estado atual é permitido; demais transições retornam 409. |
| Prioridade | baixa, media ou alta; padrão media; não aceita nulo. |
| Prazo | Data e hora ISO 8601 com fuso explícito, normalizada para UTC; padrão nulo; prazo passado é permitido. |
| Timestamps | created_at e updated_at gerados pelo servidor em UTC; created_at é imutável. |
| Versão | Inteiro iniciado em 1; incrementado a cada atualização; usado para detectar concorrência. |
| Criação | POST /tasks retorna 201 com a tarefa; campos desconhecidos ou controlados pelo servidor retornam 422. |
| Consulta | GET /tasks/{id} retorna 200 ou 404. |
| Atualização | PATCH /tasks/{id}; campos omitidos permanecem iguais; nulo limpa somente descrição e prazo. Payload sem campo editável retorna 422. ID e timestamps enviados no payload retornam 422. |
| Concorrência | PATCH e DELETE exigem expected_version. Ausência ou formato inválido retorna 422; versão desatualizada retorna 409 sem modificar o registro. |
| Exclusão | DELETE /tasks/{id} retorna 204 sem corpo; registro inexistente retorna 404. |
| Listagem no core | GET /tasks; limit padrão 20, mínimo 1, máximo 100; ordem por ID crescente; lista vazia retorna 200 com lista vazia. |
| Listagem na release 2 | Adiciona offset ≥ 0 (padrão 0), filtro status e sort por prazo ou prioridade, com direction asc ou desc. Valores inválidos retornam 422. |
| Desempate | ID crescente; prazo nulo sempre por último; prioridade asc: baixa, media, alta; desc inverte essa sequência. |
| Erros | Envelope detail com code e message; validação pode incluir errors por campo. Mensagens não expõem dados internos. |

### Testabilidade desde o core

- Injetar Repository, PriorityAdvisor e relógio no Service, permitindo substituição em testes.
- Usar banco temporário isolado por teste, sem acessar dados reais; testar persistência também com reabertura do banco.
- Cobrir contrato HTTP, limites de campos, transições, atualização parcial, nulos, 404, 409 e 422.
- Executar testes básicos a cada alteração do core; ampliar cenários nas releases seguintes.

## 9. Riscos e decisões prévias

### Persistência e concorrência — RNF-03

Antes de implementar o Repository, registrar a decisão de banco, migração inicial e limites de concorrência esperados. Escritas devem ser transacionais, com rollback em falha e verificação atômica de versão. Testar duas atualizações com a mesma versão: somente uma pode ser aplicada. Se SQLite for mantido, registrar a configuração de bloqueio e o resultado da verificação com a carga interna prevista.

### Acesso interno — RNF-01

Antes de disponibilizar o core à equipe, definir autenticação no serviço ou no gateway e autorização para leitura/escrita. Requisições sem credencial válida retornam 401; identidade autenticada sem permissão retorna 403. Proteger também documentação e sugestões de IA. Health pode ser acessível apenas na rede operacional. A revisão final confirma esses controles; não adia sua implementação.

### Dependência de IA — RF-07 e RNF-08

A IA fica desabilitada por padrão. Antes de implementar o adapter, registrar provedor, modelo, dados permitidos, limite de tokens e orçamento por período. Limites devem ser configuráveis, com bloqueio de novas chamadas ao esgotar a cota; na ausência dessas definições, manter a integração desabilitada.

Usar timeout total de 5 segundos, sem repetição automática. Enviar somente dados explicitamente permitidos da tarefa; excluir credenciais, identificadores de usuários e outros dados sensíveis. Validar resposta estruturada com prioridade enumerada e justificativa de 1 a 300 caracteres. Integração desabilitada retorna 503; timeout retorna 504; resposta inválida do provedor retorna 502. Nenhuma dessas falhas altera a tarefa ou impede o CRUD. Testar esses cenários com PriorityAdvisor simulado.
