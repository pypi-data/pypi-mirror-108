EXPOSED_HELPS += help-docker

help-docker:
	@echo "################"
	@echo "# Docker image #"
	@echo "################"
	@echo ""
	@echo "For all docker targets, you should provide a 'TAG' environment variable"
	@echo ""
	@echo "\tdocker-build-dash: Build Docker image for running Dash"
	@echo "\tdocker-build-test: Build Docker image for running tests"
	@echo ""

docker-build-dash: --check-tag
	./containers/dash/build.sh

docker-build-test: --check-tag
	./containers/tests/build.sh

--check-tag:
ifndef TAG
	$(error "You must declare TAG environment variable. \
	TAG defines the tag of the Docker image.")
endif
