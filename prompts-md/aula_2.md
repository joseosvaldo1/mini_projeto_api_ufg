## Capítulo 2 - Prompts para Codex/Copilot:

# Prompt 1 - Escopo MVP:
Contexto: MVP de micro-API de tarefas para uso de equipe interna.
Objetivo: Gerar documento de escopo com objetivo, requisitos funcionais,
não funcionais e fora de escopo.
Estilo: Linguagemk técnica, direta e em markdown.
Resposta: Gere o arquivo com o conteúdo completo em docs/escopo-mvp.md

# Prompt 2 - Backlog com releases:
Contexto: O produto será entregue em três releases: core, qualidade e
entrega final.
Objetivo: Criar backlog mínimo com IDs RF/RT e critérios de aceite.
Estilo: ChecklistMarkdown.
Resposta: Gere o arquivo com o conteúdo do backlog em docs/backlog.md.

# Prompt 3 - Arquitetura Mermaid:
Contexto: FastAPI com camadas API, Service, Repository e componentes
PriorityAdvisor.
Objetivo: Gerar diagrama Mermaid de componentes e fluxo de dados.
Resposta: Gere o arquivo em docs/arquitetura-componentes.mmd

# Prompt 4 - Conventional Commits:
Contexto: Adicionei docs/escopo-mvp.md, docs/arquitetura.md e docs/backlog.md
Objetivo: Sugerir 3 mensagens de commit no padrão Conventional Commits.
Resposta: Execute os comandos git para os três commits gerados.

# Prompt 5 - Revisão de planejamento:
Objetivo: Analise o escopo e o backlog e responda:
5.1) O que está grande demais para a release inicial?
5.2) O que está façtando para testabilidade?
5.3) Quais 3 riscos técnicosdevo mitigar antes da implementação?
Resposta: Em bullets curtos

5.1) Grande demais para a release inicial
- CORE-05 reúne consulta, filtros, ordenação e paginação; adie filtros e
ordenação, mantendo listagem limitada.
- CORE-06 reúne atualização e exclusão; separe para facilitar implementação
e aceite.
- Mantenha IA fora do core, como previsto em QUAL-05.

5.2) Falta para testabilidade
- Definir limites do título, valores padrão, transições de status e
códigos HTTP esperados.
- Especificar atualização parcial, campos nulos e desempate na ordenação.
- Prever banco isolado por teste e substituição de Repository,
PriorityAdvisor e relógio.
- Trazer testes básicos para o core; hoje estão concentrados na segunda
release.

5.3) Três riscos técnicos a mitigar
- Persistência e concorrência: definir transações, migrações e tratamento
de atualizações simultâneas.
- Acesso indevido: definir proteção da API antes do uso pela equipe; rede
interna exige controle de acesso.
- Dependência de IA: definir timeout, validação da resposta, limites de
custo e dados permitidos no envio ao provedor.
