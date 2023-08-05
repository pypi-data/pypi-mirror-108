# Landing Parsed Data

This directory should contain data from external sources with their schemas applied.
Usually, this is where you put parquet files that represent the data from the `landing/raw` directory.

`landing/parsed` structure:
```
landing
|_ parsed
  |_ <dataset_name>
    |_ <dataset_version>
      |_ dataset_file_1
      |_ dataset_file_2
```

For example:
```
landing
|_ parsed
  |_ my_super_db_export
    |_ 2020_01_01
    | |_ my_super_db_export.parquet
    |_ 2020_01_02
      |_ my_super_db_export.parquet
```
