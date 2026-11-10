# Micro-API de Gestão de Tarefas

MVP de uma API para organizar tarefas e apoiar a definição de prioridades com inteligência artificial.

## Objetivo

Centralizar o cadastro e o acompanhamento de tarefas, permitindo consultar o que precisa ser feito e receber sugestões de prioridade com base em importância, prazo e contexto. A decisão final sobre a prioridade permanece com a pessoa usuária.

## Status do projeto

O repositório está na fase de planejamento. Ainda não há código da API, manifesto de dependências ou comando de inicialização. As funcionalidades e a stack abaixo são propostas para orientar a implementação.

## Escopo do MVP

- Criar, listar, consultar, atualizar e excluir tarefas.
- Registrar título, descrição, status, prazo e prioridade.
- Filtrar tarefas por status e ordenar por prazo ou prioridade.
- Solicitar sugestões de prioridade por IA, acompanhadas de uma justificativa curta.
- Permitir aceitar ou ajustar as sugestões recebidas.

## Stack proposta

| Componente | Tecnologia | Finalidade |
| --- | --- | --- |
| Linguagem | Python 3.11 ou superior | Implementação da API |
| Framework | FastAPI | Rotas HTTP e documentação OpenAPI |
| Validação | Pydantic | Validação de entradas e saídas |
| Persistência | SQLite e SQLAlchemy | Armazenamento local das tarefas |
| Servidor | Uvicorn | Execução local da API |
| Testes | pytest | Verificação das regras e rotas |
| IA | Provedor a definir | Sugestão de prioridades |

Essas escolhas precisam ser confirmadas na primeira release. A integração de IA deverá ser configurável, mantendo a gestão básica de tarefas disponível sem credenciais de IA.

## Como rodar localmente

### Situação atual

Ainda não é possível iniciar a API neste repositório. A preparação abaixo cria apenas o ambiente Python; o serviço estará disponível após a implementação da release 0.1.

### Preparar o ambiente

Pré-requisitos: Git e Python 3.11 ou superior.

Abra um terminal na pasta do projeto e crie um ambiente virtual:

```powershell
python -m venv .venv
```

No Windows (PowerShell), ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

### Fluxo previsto após a release 0.1

A implementação deverá fornecer `requirements.txt` e o módulo `app/main.py`, com uma instância FastAPI chamada `app`. Quando esses arquivos existirem, o fluxo previsto será:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Com essa configuração, a API ficará em `http://127.0.0.1:8000` e a documentação interativa em `http://127.0.0.1:8000/docs`.

Os comandos acima descrevem a estrutura planejada e ainda não funcionam no estado atual do repositório. Deverão ser validados na entrega da release 0.1.

### Configuração da IA

O provedor, o modelo e os nomes das variáveis de ambiente serão definidos na release 0.3. Nessa etapa, será incluído um `.env.example` sem segredos, com as instruções de configuração. Credenciais reais devem permanecer fora do controle de versão.

## Roadmap de releases

Todas as releases abaixo estão planejadas, sem datas definidas.

### 0.1 — API básica

- Confirmar a stack e declarar as dependências.
- Criar a estrutura da aplicação e o modelo de tarefas.
- Implementar CRUD com persistência em SQLite.
- Disponibilizar documentação das rotas e uma rota de saúde.
- Validar os comandos de instalação e execução deste README.
- Adicionar testes das operações principais.

### 0.2 — Organização e priorização manual

- Implementar status, prazos e prioridades com validação.
- Adicionar filtros e ordenação de tarefas.
- Padronizar respostas de erro.
- Testar regras de atualização e entradas inválidas.

### 0.3 — Priorização assistida por IA

- Definir e integrar o provedor de IA.
- Gerar sugestões de prioridade e justificativas.
- Permitir revisão manual das recomendações.
- Tratar indisponibilidade e limites do serviço de IA.
- Documentar configuração, dados enviados ao provedor e exemplos de uso.

### 1.0 — Estabilização do MVP

- Consolidar testes dos fluxos principais e das falhas de integração.
- Revisar segurança e definir autenticação antes da exposição pública.
- Documentar implantação, logs e configuração do serviço.
- Publicar exemplos de requisições e critérios de aceitação do MVP.

## Estrutura atual

```text
.
├── prompts/
│   └── aulas_1.txt
├── .gitignore
└── README.md
```

A estrutura da aplicação será adicionada na release 0.1.
