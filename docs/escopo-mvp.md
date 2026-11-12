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

O serviço deve ser executado em rede ou ambiente restrito à equipe autorizada. Antes de qualquer exposição fora desse ambiente, deve haver autenticação e autorização compatíveis com a política interna. Segredos e credenciais não devem ser versionados nem registrados em logs.

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
- Atribuição de tarefas a usuários, equipes ou grupos, caso não seja necessária para o fluxo inicial.
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
