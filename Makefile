\
.PHONY: run-example clean

# Ensure uv is installed and environment is set up
setup:
	uv venv
	uv sync

# Run the basic news room example
run-example: setup
	PYTHONPATH=. uv run python examples/main.py

# Clean up Python bytecode files and __pycache__ directories
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .venv
