.PHONY: help init setup run test clean dev-setup lint format install

# Default target
help:
	@echo "Nationwide Balance Viewer - Build Commands"
	@echo "=========================================="
	@echo "init        Initialize project configuration (create settings.ini)"
	@echo "setup       Create venv and install dependencies"
	@echo "run         Run the application"
	@echo "test        Run test suite"
	@echo "clean       Clean build artifacts and cache"
	@echo "dev-setup   Setup with development dependencies"
	@echo "lint        Run code linting"
	@echo "format      Format code"
	@echo "install     Install package in development mode"

# Initialize project configuration (not git)
init: settings.ini
	@echo "✓ Project initialized"

settings.ini: settings.ini.template
	@if [ ! -f settings.ini ]; then \
		cp settings.ini.template settings.ini; \
		echo "✓ Created settings.ini from template"; \
		echo "Please edit settings.ini with your preferences"; \
	else \
		echo "✓ settings.ini already exists"; \
	fi

# Create virtual environment and install dependencies
setup: venv/bin/activate requirements.txt
	@echo "✓ Virtual environment ready"

venv/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	python3.11 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "✓ Dependencies installed"

# Run the application
run: venv/bin/activate settings.ini
	./venv/bin/python -m src.cli

# Run tests
test: venv/bin/activate
	./venv/bin/python -m pytest tests/ -v

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

# Development setup with additional tools
dev-setup: setup
	./venv/bin/pip install pytest black flake8 mypy

# Lint code
lint: venv/bin/activate
	./venv/bin/flake8 src/ tests/
	./venv/bin/mypy src/

# Format code
format: venv/bin/activate
	./venv/bin/black src/ tests/

# Install in development mode
install: venv/bin/activate
	./venv/bin/pip install -e .
