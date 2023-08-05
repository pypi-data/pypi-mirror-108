EXPOSED_HELPS += help-examples

help-examples:
	@echo "############"
	@echo "# Examples #"
	@echo "############"
	@echo ""
	@echo "\tgenerate-example: Run jupyter notebook"
	@echo ""

generate-example:
	mkdir -p workdir/landing/raw/dataset_example/version_1
	echo "id,value" > workdir/landing/raw/dataset_example/version_1/example.csv
	echo "1,toto" >> workdir/landing/raw/dataset_example/version_1/example.csv
	echo "2,titi" >> workdir/landing/raw/dataset_example/version_1/example.csv
