
CONTAINER_NAME=fastapi_app

CODE_DIR=app

TEST_DIR=tests

PYTEST_OPTS=--cov=$(CODE_DIR) --cov-report=term

.PHONY: test

test:
	docker exec -it $(CONTAINER_NAME) pytest $(PYTEST_OPTS)
