.PHONY: help install serve test
.DEFAULT_GOAL := help

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv sync --all-extras

serve: ## Run server
	@echo "🛑 Killing any existing Flask processes..."
	@pkill -9 -f "python.*main.py" 2>/dev/null || true
	@sleep 1
	@echo "🚀 Starting ScrapDDL server (with increased file limit)..."
	@sh -c 'ulimit -n 4096 && uv run python scrapddl/main.py'

test: ## Run tests
	uv run pytest scrapddl/tests
