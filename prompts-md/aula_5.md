## Capítulo 5 - Prompts para Codex/Copilot:

# Prompt 1 - Makefile:
Contexto: Projeto FastAPI com comandos de instalar dependências,
executar API e rodar testes.
Objetivo: Gerar Makefile com target install, run e teste.
Estilo: Simples e portável.
Resposta: Crie o arquivo completo Makefile no raiz do projeto.

# Prompt 2 - .env-example:
Contexto: O projeto usa integração opcional de LLM.
Objetivo: Criar arquivo .env-example com variáveis necessárias e
valores placeholder seguros.
Estilo: Minimalista.
Resposta: Gere o arquivo .env-example na raiz do projeto.

# Prompt 3 - Revisão de README:
Contexto: Analise meu README atual e responda:
I) O que falta para ser reproduzível em máquina local?
II) Quais seções estão fracas para onboarding tecnico?
III) Como melhorar a seção de uso da IA?
Resposta: Em checklist objetivo.

* Checklist:

I) Reprodutibilidade em máquina local

- [ ] Documentar uma sequência única para instalar, iniciar e testar, de
preferência usando make install, make run e make teste.
- [ ] Explicar como instalar e usar make no Windows, ou oferecer comandos
Python equivalentes.
- [ ] Incluir uma verificação de saúde após iniciar, como acessar /health.
- [ ] Explicar onde o SQLite tasks.db é criado e como resetar os dados
locais.
- [ ] Revisar requirements-dev.txt: ele lista httpx2, mas o README menciona
HTTPX para TestClient.
- [ ] Documentar como usar .env-example e esclarecer que o código lê variáveis
do ambiente do processo; não foi identificado carregamento automático de .env.

II) Seções fracas para onboarding técnico

- [ ] Instalação: incluir a ativação do ambiente virtual em Linux/macOS.
- [ ] Arquitetura: explicar como visualizar o diagrama ou incluir uma
imagem renderizada.
- [ ] Modelo e endpoints: incluir exemplos de erros e explicar a diferença
entre PUT e PATCH, se ambos estiverem disponíveis.
- [ ] Exemplos de uso: mostrar uma resposta de criação e esclarecer que os
UUIDs são ilustrativos.
- [ ] Desenvolvimento: documentar formatação, convenções e um comando curto
para executar os testes.
- [ ] Estado atual: manter rotas e limitações sincronizadas com o código.

III) Melhorias na seção de uso da IA

- [ ] Separar o funcionamento local por heurística do uso remoto da OpenAI e
esclarecer que não há endpoint HTTP para o advisor.
- [ ] Explicar como configurar a chave no ambiente do processo e que .env-example
não é carregado automaticamente pelo código atual.
- [ ] Informar os valores padrão de OPENAI_MODEL e OPENAI_RESPONSES_URL e
como substituí-los.
- [ ] Descrever os dados enviados (título e descrição), o uso de store: false
e a possibilidade de custos.
- [ ] Explicar o fallback para a heurística local quando a chamada remota
falha.
- [ ] Esclarecer o alias legado OPEAN_API_KEY, cuja grafia parece um erro
tipográfico.
- [ ] Confirmar o nome do modelo TasjOut no exemplo de código e garantir
que o exemplo seja executável.

# Prompt 4 - Checklist de release:
Contexto: Vou publicar a versão v1.0.0 no GutHub.
Objetivo: Gerar checklist final com itens técnicos e de documentação
para release.
Estilo: Cheklist Markdown.
Resposta: Lista completa.

## Checklist de release v1.0.0

### Código e controle de versão

- [ ] Confirmar que o branch de release contém os commits esperados e
está atualizado com o remoto.
- [ ] Revisar git status e decidir o que fazer com as alterações locais
pendentes, incluindo exclusões em prompts/aula_1.txt a prompts/aula_4.txt,
prompts-md/ e tasks.db.
- [ ] Conferir que arquivos temporários, bancos locais e segredos não
serão publicados.
- [ ] Confirmar que .env-example contém apenas placeholders e que .env
está no .gitignore.
- [ ] Escolher e aplicar uma tag consistente, como v1.0.0, apontando
para o commit aprovado.
- [ ] Preparar notas de release com mudanças, limitações conhecidas e
instruções de atualização.

### Reprodutibilidade e dependências

- [ ] Confirmar suporte a Python 3.11 ou superior em Windows, Linux e macOS.
- [ ] Conferir requirements.txt e requirements-dev.txt, incluindo a dependência
HTTPX usada pelo TestClient.
- [ ] Criar um ambiente virtual limpo e executar a instalação documentada.
- [ ] Confirmar se GNU Make estará disponível para o público alvo; manter os
comandos Python equivalentes documentados.
- [ ] Verificar se as instruções de instalação, execução e testes funcionam
em cada sistema operacional suportado.

### Verificação técnica

- [ ] Executar toda a suíte: make teste ou o comando Pytest documentado.
- [ ] Iniciar a API com make run e verificar /health, /docs e /redoc.
- [ ] Exercitar o CRUD: criação, listagem paginada, consulta, substituição
e exclusão.
- [ ] Conferir respostas esperadas para dados inválidos (422), task inexistente
(404) e exclusão bem-sucedida (204).
- [ ] Validar a persistência SQLite e o comportamento quando o banco ainda
não existe.
- [ ] Testar a heurística local de prioridade sem chave de API.
- [ ] Se a integração remota fizer parte da release, testar chave válida,
timeout/falha e fallback local sem expor a chave nos logs.
- [ ] Confirmar que o exemplo TasjOut no README roda com a versão atual
do código.

### Segurança e escopo

- [ ] Reforçar nas notas que a API não possui autenticação; mantê-la restrita
a uso local ou protegido.
- [ ] Não publicar a API aberta à internet sem adicionar autenticação e controles
de acesso.
- [ ] Confirmar que nenhum dado de demonstração ou pessoal do tasks.db será
incluído.
- [ ] Documentar que chamadas à OpenAI podem gerar custos e que não há limite
de gastos implementado.
- [ ] Confirmar que o README explica quais dados da task são enviados e que a
requisição usa store: false.

### Documentação e publicação no GitHub

- [ ] Conferir ortografia, links internos, comandos, tabelas e blocos de
código do README.
- [ ] Confirmar que .env-example é identificado como modelo e que não há promessa
de carregamento automático de .env.
- [ ] Verificar o diagrama docs/arquitetura-componentes.mmd em um visualizador
Mermaid.
- [ ] Adicionar ou revisar licença, se o repositório ainda não tiver uma.
- [ ] Confirmar que a descrição da release distingue recursos implementados de
limitações e próximos passos.
- [ ] Publicar a tag e criar a release v1.0.0 no GitHub com as notas finais.


# Prompt 5 - Script de demo tecnica:
