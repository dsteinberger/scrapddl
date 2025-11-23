.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

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

test: ## Run test
	uv run pytest scrapddl/tests
