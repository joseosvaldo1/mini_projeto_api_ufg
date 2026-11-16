.PHONY: install run teste

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements-dev.txt

run:
	$(PYTHON) -m uvicorn app.main:app --reload

teste:
	$(PYTHON) -m pytest -q tests/test_core_api.py tests/test_task_service.py tests/test_task_routes.py tests/test_priority_advisor.py
