

.PHONY: requirements.txt
requirements.txt:
	poetry export -o requirements.txt --without-hashes
