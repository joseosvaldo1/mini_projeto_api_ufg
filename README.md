# Micro-API de Tarefas

API REST em FastAPI para criar, listar, consultar, substituir e excluir tarefas. Os dados ficam em SQLite. A sugestão de prioridade pode usar uma heurística local ou, quando configurada, a API da OpenAI.

## Estado atual

- CRUD disponível em `/tasks` e verificação de saúde em `/health`.
- A sugestão de prioridade existe no serviço Python, mas não possui endpoint HTTP e não é chamada pelo CRUD.
- A tarefa contém título, descrição e conclusão. Não há status de fluxo, prazo ou prioridade persistida.
- Não há autenticação; mantenha a API em ambiente local ou protegido.

## Requisitos

- Python 3.11 ou superior
- pip
- GNU Make, se quiser usar os alvos `make` (opcional)
- Git, para clonar o repositório

## Instalação e execução local

Execute os comandos a partir da raiz do repositório. O Makefile oferece os comandos curtos; os comandos Python equivalentes estão abaixo.

### Opção recomendada: Make

```sh
make install
make run
```

No Windows, é necessário ter GNU Make disponível no `PATH`. Se não tiver, use os comandos diretos desta seção.

### Comandos diretos

Crie e ative um ambiente virtual:

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```sh
# Linux ou macOS
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências de runtime, teste e desenvolvimento:

```sh
python -m pip install -r requirements-dev.txt
```

Inicie a API em modo de desenvolvimento:

```sh
python -m uvicorn app.main:app --reload
```

O servidor fica em `http://127.0.0.1:8000`. Acesse `/docs` para a interface OpenAPI, `/redoc` para a referência ReDoc e `/health` para verificar a disponibilidade. Uma resposta saudável tem `status: "ok"`.

### Banco local

O SQLite é salvo como `tasks.db` no diretório de trabalho atual. Inicie a API a partir da raiz do projeto para manter o banco ali. Para reiniciar os dados de demonstração, pare o servidor, faça uma cópia de segurança se precisar dos dados e então remova `tasks.db`; o banco será recriado na próxima inicialização.

## Testes e desenvolvimento

Com o ambiente virtual ativo e as dependências instaladas, execute:

```sh
make teste
```

Comando equivalente:

```sh
python -m pytest -q tests/test_core_api.py tests/test_task_service.py tests/test_task_routes.py tests/test_priority_advisor.py
```

Os testes usam bancos SQLite temporários e simulam as chamadas externas do advisor. Não precisam de chave da OpenAI nem devem fazer chamadas reais à API. O repositório não configura atualmente formatador ou linter; mantenha o estilo existente e inclua testes para mudanças de comportamento.

## Arquitetura

```text
app/
├── main.py                       # Cria a aplicação e monta o router
├── api/task_routes.py             # Rotas HTTP, status e validação
├── model/tasks.py                 # Modelos de entrada, saída e sugestão
├── repositories/                  # Contrato e persistência SQLite
└── services/                      # Regras de negócio e advisor de prioridade
tests/                              # Testes de API, serviço, persistência e advisor
```

O fluxo CRUD passa das rotas para `TaskService`, que usa o protocolo do repositório; a implementação atual persiste em SQLite. As dependências concretas são montadas por `get_task_service`. O diagrama está em [docs/arquitetura-componentes.mmd](docs/arquitetura-componentes.mmd); abra-o em um visualizador compatível com Mermaid ou como texto Markdown.

## Modelo e endpoints

Exemplo de resposta de tarefa (o UUID é ilustrativo):

```json
{
  "id": "8bd67cc3-c286-4bc0-97d5-7d88775693c8",
  "title": "Revisar a release",
  "description": null,
  "completed": false
}
```

- `id`: UUID gerado pelo servidor.
- `title`: obrigatório; espaços nas extremidades são removidos; de 1 a 200 caracteres.
- `description`: opcional na criação, pode ser `null` e aceita até 2.000 caracteres.
- `completed`: booleano estrito; padrão `false` na criação.

| Método | Caminho | Descrição | Respostas principais |
| --- | --- | --- | --- |
| GET | `/health` | Estado e timestamp UTC do serviço | 200 |
| POST | `/tasks` | Cria uma tarefa | 201, 422 |
| GET | `/tasks` | Lista tarefas paginadas | 200, 422 |
| GET | `/tasks/{task_id}` | Consulta por UUID | 200, 404, 422 |
| PUT | `/tasks/{task_id}` | Substitui os campos editáveis | 200, 404, 422 |
| DELETE | `/tasks/{task_id}` | Exclui uma tarefa | 204, 404, 422 |

`GET /tasks` aceita `limit` (padrão 20, de 1 a 100) e `offset` (padrão 0, mínimo 0). O `PUT` substitui o conjunto de campos editáveis e exige `title`, `description` (que pode ser `null`) e `completed`. Não existe rota `PATCH`. UUID inválido, corpo inválido ou parâmetro fora dos limites retorna 422. UUID válido sem tarefa retorna 404 com `{"detail":"Task not found."}`. Os demais erros usam o formato padrão do FastAPI, sem envelope próprio.

## Exemplos de uso HTTP

Criar tarefa (a resposta 201 contém o UUID real a usar nas chamadas seguintes):

```sh
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Revisar a release","description":null,"completed":false}'
```

Listar uma página:

```sh
curl "http://127.0.0.1:8000/tasks?limit=20&offset=0"
```

Para consultar, substituir ou excluir, troque `<id-da-resposta>` pelo `id` retornado ao criar:

```sh
curl http://127.0.0.1:8000/tasks/<id-da-resposta>

curl -X PUT http://127.0.0.1:8000/tasks/<id-da-resposta> \
  -H "Content-Type: application/json" \
  -d '{"title":"Release revisada","description":"Pronta para publicar","completed":true}'

curl -X DELETE http://127.0.0.1:8000/tasks/<id-da-resposta>
```

## Sugestão de prioridade e uso da IA

`PriorityAdvisor.suggest_priority(task)` retorna `baixa`, `media` ou `alta` e uma justificativa curta. A sugestão não altera nem persiste a tarefa. Ela pode ser chamada diretamente pelo serviço Python; não há endpoint HTTP para solicitar uma sugestão e o CRUD não invoca o advisor.

Sem chave, é usada uma heurística local: termos como “urgente”, “incidente” ou “hoje” indicam prioridade alta; frases como “sem pressa” ou “melhoria futura” indicam baixa; nos demais casos, a prioridade é média. A execução local não exige rede nem credenciais.

Exemplo executável no nível de serviço (o nome `TasjOut` é o nome atual da classe de saída):

```python
from app.model.tasks import TasjOut
from app.services.priority_advisor import PriorityAdvisor

task = TasjOut(
    title="Incidente urgente no serviço",
    description="A aplicação está indisponível.",
    completed=False,
)
suggestion = PriorityAdvisor().suggest_priority(task)
print(suggestion.priority)
print(suggestion.justification)
```

### Configurar a integração opcional com OpenAI

Para habilitar a chamada remota, configure `OPENAI_API_KEY` no ambiente do processo antes de iniciar a aplicação. `.env-example` é apenas um modelo de variáveis: o código atual não carrega automaticamente arquivos `.env`. Copie os nomes e valores necessários para o ambiente seguro da sua máquina; não versione nem compartilhe a chave.

```powershell
# Windows PowerShell: vale para esta sessão do terminal
$env:OPENAI_API_KEY = "sua-chave"
```

```sh
# Linux ou macOS: vale para esta sessão do terminal
export OPENAI_API_KEY="sua-chave"
```

| Variável | Padrão | Uso |
| --- | --- | --- |
| `OPENAI_API_KEY` | Não definido | Habilita a solicitação remota quando não está vazia. |
| `OPENAI_MODEL` | `gpt-6-luna` | Modelo solicitado. |
| `OPENAI_RESPONSES_URL` | `https://api.openai.com/v1/responses` | URL da Responses API. |

O código também aceita `OPEAN_API_KEY`, uma grafia legada mantida por compatibilidade; prefira `OPENAI_API_KEY` em novas configurações. A requisição envia o título e a descrição da tarefa, pede uma resposta JSON estruturada e usa `store: false`. Uma chamada com chave pode gerar custo de API. O timeout é de 5 segundos. Se a rede, a resposta ou a validação falhar, um aviso é registrado e a heurística local é usada como fallback.

## Limitações e segurança

- Não há autenticação ou autorização; mantenha o serviço local ou atrás de controles de acesso antes de qualquer uso compartilhado.
- O advisor de prioridade não possui endpoint HTTP e não é chamado pelo CRUD.
- A tarefa ainda não armazena status de fluxo, prioridade ou prazo.
- SQLite é a persistência atual; não há migrações, estratégia de backup ou teste de carga concorrente.
- Não há controle otimista de concorrência nem versão de registro.
- A listagem tem paginação por limite e offset, mas não oferece filtros ou ordenação por status, prazo ou prioridade.
- Erros HTTP seguem os detalhes padrão do FastAPI, sem formato padronizado próprio.
- A integração com LLM é opcional e não tem cota nem limite de gastos implementado.
