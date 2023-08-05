EXPOSED_HELPS += help-sync

help-sync:
	@echo "###############"
	@echo "# Manage Data #"
	@echo "###############"
	@echo ""
	@echo "\tsync-raw-data-local-to-s3: Synchronize raw data from local disk to S3 bucket"
	@echo "\tsync-raw-data-s3-to-local: Synchronize raw data from S3 bucket to local disk"
	@echo ""

sync-raw-data-local-to-s3:
	aws s3 sync workdir/landing/raw s3://{{projectSlug}}-data/landing/raw

sync-raw-data-s3-to-local:
	aws s3 sync s3://{{projectSlug}}-data/landing/raw workdir/landing/raw

destroy-aws-infrastructure:
	./scripts/destroy-aws-infrastructure.bash
