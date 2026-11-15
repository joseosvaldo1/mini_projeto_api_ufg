# Micro-API de Tarefas

API REST em FastAPI para cadastrar, consultar, atualizar e excluir tarefas. O projeto inclui persistência SQLite, validação com Pydantic e um advisor de prioridade que funciona localmente e pode usar a API da OpenAI quando uma chave estiver configurada.

## Estado atual

O CRUD e a rota de saúde estão disponíveis. A sugestão de prioridade existe no nível de serviço, mas ainda não há endpoint HTTP para solicitá-la. O modelo de tarefa atual contém título, descrição e estado de conclusão; status de fluxo, prazo e prioridade persistida ainda não fazem parte do CRUD.

## Requisitos

- Python 3.11 ou superior
- pip
- Git (para obter o repositório)

## Instalação

Na raiz do projeto, crie e ative um ambiente virtual.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Para instalar também as ferramentas de desenvolvimento e teste:

```powershell
python -m pip install -r requirements-dev.txt
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` inclui as dependências de runtime, Pytest e HTTPX para o TestClient.

## Executar a API

A partir da raiz do projeto, com o ambiente virtual ativo:

```bash
python -m uvicorn app.main:app --reload
```

Endereços locais:

- API: http://127.0.0.1:8000
- OpenAPI interativo: http://127.0.0.1:8000/docs
- Referência ReDoc: http://127.0.0.1:8000/redoc
- Saúde: http://127.0.0.1:8000/health

A aplicação usa `tasks.db` no diretório de trabalho atual. Execute o servidor a partir da raiz do projeto para manter o banco nesse local.

## Testes

Com as dependências de desenvolvimento instaladas, execute a suíte completa explicitando os módulos:

```bash
python -m pytest -q tests/test_core_api.py tests/test_task_service.py tests/test_task_routes.py tests/teste_priority_advisor.py
```

A suíte usa bancos SQLite temporários e simula chamadas externas do advisor; não precisa de chave de API nem deve fazer chamadas reais à OpenAI.

## Arquitetura

```text
app/
├── main.py                       # Cria a aplicação e monta o router
├── api/
│   └── task_routes.py             # Rotas HTTP, status e validação de parâmetros
├── model/
│   └── tasks.py                   # Modelos de entrada, saída e sugestão
├── repositories/
│   ├── protocols.py               # Contrato do repositório
│   └── task_repository.py         # Persistência SQLite
└── services/
    ├── task_service.py            # Regras de negócio e coordenação
    └── priority_advisor.py        # Heurística local e integração opcional com LLM

tests/                              # Testes de API, serviço, persistência e advisor
```

O fluxo CRUD passa das rotas para `TaskService`, que usa o protocolo do repositório; a implementação atual persiste em SQLite. As dependências concretas são montadas pela dependência `get_task_service` das rotas. O diagrama está em [docs/arquitetura-componentes.mmd](docs/arquitetura-componentes.mmd).

## Modelo de tarefa

Exemplo de resposta:

```json
{
  "id": "8bd67cc3-c286-4bc0-97d5-7d88775693c8",
  "title": "Revisar a release",
  "description": null,
  "completed": false
}
```

Regras atuais:

- `id`: UUID gerado pelo servidor.
- `title`: obrigatório; espaços nas extremidades são removidos; deve ter de 1 a 200 caracteres depois da remoção.
- `description`: opcional na criação, pode ser nula e aceita até 2.000 caracteres.
- `completed`: booleano; padrão `false` na criação.

O endpoint `PUT` substitui os campos editáveis e exige `title`, `description` (pode ser `null`) e `completed` no corpo.

## Endpoints

| Método | Caminho | Descrição | Respostas principais |
| --- | --- | --- | --- |
| GET | `/health` | Estado e timestamp UTC do serviço | 200 |
| POST | `/tasks` | Cria uma tarefa | 201, 422 |
| GET | `/tasks` | Lista tarefas paginadas | 200, 422 |
| GET | `/tasks/{task_id}` | Consulta por UUID | 200, 404, 422 |
| PUT | `/tasks/{task_id}` | Substitui os campos editáveis | 200, 404, 422 |
| DELETE | `/tasks/{task_id}` | Exclui uma tarefa | 204, 404, 422 |

A listagem aceita:

- `limit`: padrão 20, mínimo 1 e máximo 100.
- `offset`: padrão 0 e mínimo 0.

UUID malformado, corpo inválido ou parâmetro fora dos limites retorna 422. Um UUID válido sem tarefa correspondente retorna 404 com `{"detail":"Task not found."}`. A API ainda usa os erros padrão do FastAPI e não possui um envelope de erro próprio.

## Exemplos de uso

Criar tarefa:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Revisar a release","description":null,"completed":false}'
```

Listar uma página:

```bash
curl "http://127.0.0.1:8000/tasks?limit=20&offset=0"
```

Consultar uma tarefa:

```bash
curl http://127.0.0.1:8000/tasks/8bd67cc3-c286-4bc0-97d5-7d88775693c8
```

Substituir uma tarefa:

```bash
curl -X PUT http://127.0.0.1:8000/tasks/8bd67cc3-c286-4bc0-97d5-7d88775693c8 \
  -H "Content-Type: application/json" \
  -d '{"title":"Release revisada","description":"Pronta para publicar","completed":true}'
```

Excluir uma tarefa:

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/8bd67cc3-c286-4bc0-97d5-7d88775693c8
```

## Sugestão de prioridade

`PriorityAdvisor.suggest_priority(task)` retorna uma sugestão com prioridade `baixa`, `media` ou `alta` e uma justificativa curta. A sugestão não altera nem persiste a tarefa.

Sem chave configurada, o advisor usa uma heurística local: termos como “urgente”, “incidente” ou “hoje” apontam para alta; frases como “sem pressa” ou “melhoria futura” apontam para baixa; nos demais casos, a prioridade é média.

Exemplo no código:

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

### Integração opcional com OpenAI

A chamada externa só é tentada quando o processo tem uma chave não vazia em uma destas variáveis:

- `OPENAI_API_KEY` (nome recomendado)
- `OPEAN_API_KEY` (alias mantido para compatibilidade com a grafia anterior)

A chave deve ser configurada no ambiente do processo, nunca versionada no repositório. Por exemplo:

```powershell
$env:OPENAI_API_KEY = "<sua-chave>"
```

```bash
export OPENAI_API_KEY="<sua-chave>"
```

Configuração opcional:

| Variável | Padrão | Uso |
| --- | --- | --- |
| `OPENAI_MODEL` | `gpt-6-luna` | Modelo solicitado |
| `OPENAI_RESPONSES_URL` | `https://api.openai.com/v1/responses` | Endpoint da Responses API |

A chamada envia o título e a descrição, usa formato de resposta estruturado e timeout de 5 segundos. Se a chamada ou a validação da resposta falhar, o advisor registra um aviso e retorna a sugestão local. Com uma chave configurada, cada solicitação de sugestão pode gerar custo de API. Não há cota nem limite de gastos implementado.

## Limitações e segurança

- Não há autenticação ou autorização. Restrinja o serviço a ambiente local ou protegido por controles externos; não o exponha publicamente.
- A sugestão de prioridade não possui endpoint HTTP e não é chamada pelo CRUD.
- A tarefa ainda não armazena status de fluxo, prioridade ou prazo.
- SQLite é a persistência atual; não há migrações, estratégia de backup ou teste de carga concorrente.
- Não há controle otimista de concorrência nem versão de registro.
- A listagem tem paginação por limite e offset, mas ainda não oferece filtros ou ordenação por status, prazo ou prioridade.
- Erros HTTP não seguem um formato padronizado além dos detalhes padrão do FastAPI.

## Próximos passos

1. Definir autenticação e autorização antes do uso compartilhado.
2. Expandir o modelo com status, prazo e prioridade persistida, incluindo regras de transição.
3. Adicionar um endpoint HTTP para solicitar sugestões e documentar os dados enviados.
4. Implementar concorrência otimista, migrações, configuração do caminho do banco e backup/restore.
5. Padronizar erros, expandir a cobertura de regressão e automatizar os testes no fluxo de integração contínua.
6. Definir limites de uso e orçamento para a integração opcional com LLM.
