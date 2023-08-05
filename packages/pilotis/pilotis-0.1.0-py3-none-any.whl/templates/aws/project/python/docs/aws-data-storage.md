# Synchronizing data from and to AWS storage

## Requirements

Every command that interact with AWS will use AWS credentials.
If you don't have any, please ask the infrastructure owner.
Set them using:

```bash
cd infrastructure
cp set_aws_credentials.bash.template .secrets/set_aws_credentials.bash
chmod u+x .secrets/set_aws_credentials.bash
vim .secrets/set_aws_credentials.bash
source .secrets/set_aws_credentials.bash 
```

## Synchronize DATA from AWS S3

To get raw data from s3, run:

```bash
make sync-raw-data-s3-to-local
```

## Synchronize DATA to AWS S3

To send local raw data to s3, run:

```bash
make sync-raw-data-local-to-s3
```

# Delete generated infrastructure

To delete the generated infrastructure, run:

```bash
make destroy-aws-infrastructure
```
