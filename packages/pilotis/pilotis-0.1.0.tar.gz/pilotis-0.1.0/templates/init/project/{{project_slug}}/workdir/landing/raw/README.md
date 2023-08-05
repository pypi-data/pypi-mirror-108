# Landing Raw Data

This directory should contain data from external sources in their raw format.

`landing/raw` structure:
```
landing
|_ raw
  |_ <dataset_name>
    |_ <dataset_version>
      |_ dataset_file_1
      |_ dataset_file_2
```

For example:
```
landing
|_ raw
  |_ my_super_db_export
    |_ 2020_01_01
    | |_ export_20200101_part_1.csv
    | |_ export_20200101_part_2.csv
    |_ 2020_01_02
      |_ export_20200102.csv
```
