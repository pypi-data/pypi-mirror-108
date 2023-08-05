import pandas as pd
from pilotis_io.directory_structure import dataset_raw_dir_path
from pilotis_io.io import IoAPI
from pilotis_io.pandas import PandasApi
from pilotis_io.persistence import LandingDataSourcePersistence

COLUMN_NAME_VALUE = "value"
COLUMN_NAME_ID = "id"


class DatasetExamplePersistence(LandingDataSourcePersistence):
    schema = {COLUMN_NAME_ID: int, COLUMN_NAME_VALUE: str}

    def __init__(self, io_api: IoAPI, pandas_api: PandasApi) -> None:
        super().__init__(io_api, pandas_api, "dataset_example")

    def load_raw(self, dataset_version: str = None) -> pd.DataFrame:
        dataset_files = self.io_api.list_files_in_dir(
            dataset_raw_dir_path(self.dataset_name, dataset_version)
        )
        return self.pandas_api.load_pandas_dataset(
            dataset_files, sep=",", header=0, dtype=self.schema
        )
