EXPOSED_HELPS += help-docs

help-docs:
	@echo "#################"
	@echo "# Documentation #"
	@echo "#################"
	@echo ""
	@echo "\tdoc-site: Generates and run tht documentation website"
	@echo ""

doc-site:
	cd python && poetry run mkdocs serve
