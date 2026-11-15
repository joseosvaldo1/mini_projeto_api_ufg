from urllib.error import URLError

import pytest

from app.model.tasks import TasjOut
from app.services.priority_advisor import PriorityAdvisor


@pytest.mark.parametrize(
    ("title", "description", "expected_priority"),
    [
        ("Incidente urgente", None, "alta"),
        ("Revisar documentação", "Adicionar seção de configuração", "media"),
        ("Melhoria futura", "Sem pressa para esta tarefa", "baixa"),
    ],
)
def test_local_heuristic_suggests_each_priority_level(
    monkeypatch: pytest.MonkeyPatch,
    title: str,
    description: str | None,
    expected_priority: str,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPEAN_API_KEY", raising=False)
    task = TasjOut(title=title, description=description, completed=False)

    suggestion = PriorityAdvisor().suggest_priority(task)

    assert suggestion.priority == expected_priority
    assert suggestion.justification


def test_failed_external_call_falls_back_to_local_heuristic(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    task = TasjOut(
        title="Incidente urgente no serviço",
        description="O sistema está indisponível.",
        completed=False,
    )

    def fail_request(*args: object, **kwargs: object) -> None:
        raise URLError("simulated API outage")

    monkeypatch.setattr(
        "app.services.priority_advisor.urlopen",
        fail_request,
    )

    suggestion = PriorityAdvisor().suggest_priority(task)

    assert suggestion.priority == "alta"
    assert suggestion.justification
    assert "using local heuristic" in caplog.text
