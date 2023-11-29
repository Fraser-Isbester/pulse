
requirements.txt: poetry.lock
	poetry export -o requirements.txt --with dev

.PHONY: clean-cache
clean-cache:  ## Deletes every __pycache__ folder in the project
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: test
test:
	@python -m pytest tests/unit

.PHONY: lint
lint:  ## Lints ./pulse fixes everthing it can safely in the processes
	@ruff ./pulse
