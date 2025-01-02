DC=docker-compose
CONTAINER_NAME=fastapi_app
CODE_DIR=app
PYTEST_OPTS=--cov=$(CODE_DIR) --cov-report=term

.PHONY: tests tests-cov app app-down

tests:
	docker exec -it $(CONTAINER_NAME) pytest

tests-cov:
	docker exec -it $(CONTAINER_NAME) pytest $(PYTEST_OPTS)

app:
	$(DC) up --build -d

app-down:
	${DC} down