.PHONY: help install setup db-up db-down migrate test run clean check

help:
	@echo "Smart Blood Bank - Available Commands"
	@echo "======================================"
	@echo "make install    - Install Python dependencies"
	@echo "make setup      - Initial project setup"
	@echo "make check      - Check environment setup"
	@echo "make db-up      - Start PostgreSQL with Docker"
	@echo "make db-down    - Stop PostgreSQL"
	@echo "make migrate    - Run database migrations"
	@echo "make test       - Run tests"
	@echo "make run        - Start development server"
	@echo "make clean      - Clean temporary files"

install:
	cd backend && pip install -r requirements.txt

setup: install
	cp .env.example .env
	@echo "✓ Setup complete! Edit .env with your configuration."

check:
	python scripts/check_setup.py

db-up:
	docker-compose up -d db

db-down:
	docker-compose down

migrate:
	cd backend && alembic upgrade head

test:
	cd backend && pytest ../tests/ -v

run:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".hypothesis" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
