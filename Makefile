.PHONY: help dev build test test-int test-e2e test-load lint format migrate seed clean docker-up docker-down

# Default target
help:
	@echo "douyin-fashion-ai - Available commands:"
	@echo ""
	@echo "  make dev          Start all services in development mode"
	@echo "  make build        Build all services"
	@echo "  make test         Run unit tests"
	@echo "  make test-int     Run integration tests"
	@echo "  make test-e2e     Run end-to-end tests"
	@echo "  make test-load    Run load tests"
	@echo "  make lint         Lint all code"
	@echo "  make format       Format all code"
	@echo "  make migrate      Run database migrations"
	@echo "  make seed         Seed demo data and templates"
	@echo "  make docker-up    Start Docker Compose stack"
	@echo "  make docker-down  Stop Docker Compose stack"
	@echo "  make clean        Remove build artifacts"

# Development
dev:
	@echo "Starting development servers..."
	npm run dev

docker-up:
	docker-compose up -d
	@echo "All services started. API: http://localhost:8000 | Web: http://localhost:3000"

docker-down:
	docker-compose down

# Build
build:
	@echo "Building all services..."
	npm run build

# Testing
test:
	@echo "Running unit tests..."
	npm run test:unit

pytest-unit:
	pytest tests/unit -v --tb=short

test-int:
	@echo "Running integration tests..."
	npm run test:integration
	pytest tests/integration -v --tb=short

test-e2e:
	@echo "Running end-to-end tests..."
	npm run test:e2e

test-load:
	@echo "Running load tests..."
	python scripts/benchmark/run_load_test.py

test-prompts:
	@echo "Running prompt regression tests..."
	python -m pytest prompts/tests/ -v

# Code quality
lint:
	@echo "Linting code..."
	npm run lint
	ruff check services/ workers/

format:
	@echo "Formatting code..."
	npm run format
	ruff format services/ workers/
	black services/ workers/

# Database
migrate:
	@echo "Running database migrations..."
	python scripts/migrations/run.py

migrate-down:
	@echo "Rolling back last migration..."
	python scripts/migrations/run.py --rollback

# Seeding
seed:
	@echo "Seeding demo data and templates..."
	python scripts/seed/seed_templates.py
	python scripts/seed/seed_demo_tenant.py

# Smoke tests
smoke:
	@echo "Running smoke tests against running stack..."
	python scripts/smoke/run_smoke.py

# Benchmarks
benchmark:
	@echo "Running inference cost and latency benchmarks..."
	python scripts/benchmark/run_benchmark.py

# Clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf dist/ build/ .next/ __pycache__/ .pytest_cache/
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# Docker build
docker-build:
	docker-compose build

# Logs
logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api-gateway

logs-worker:
	docker-compose logs -f video-worker

# Install
install:
	npm install
	pip install -r services/requirements.txt
	pip install -r workers/requirements.txt
