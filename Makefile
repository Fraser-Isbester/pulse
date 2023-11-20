

.PHONY: requirements.txt
requirements.txt:
	poetry export -o requirements.txt --without-hashes

.PHONY: clean-cache
clean-cache:  ## Deletes every __pycache__ folder in the project
	find . -type d -name "__pycache__" -exec rm -rf {} +
