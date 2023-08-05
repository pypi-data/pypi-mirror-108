EXPOSED_HELPS += help-config

help-config:
	@echo "##################"
	@echo "# Configurations #"
	@echo "##################"
	@echo ""
	@echo "\tcheck-tools: Validate that all required tools are correctly installed and configured"
	@echo "\tsetup-env: Configure all required tools"
	@echo ""

check-tools:
	./scripts/check_tools.bash

setup-env:
	cd python && make pyenv-config
	make check-tools
	cd python && make setup-env-full
