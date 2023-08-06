from typing import Dict
from typing import Union

from pyspark.sql import DataFrame

from tecton._internals import errors
from tecton.interactive.virtual_data_source import VirtualDataSource

VALID_DATA_SOURCE_TYPES = [VirtualDataSource]
VALID_DATA_FRAME_TYPES = [DataFrame]


class DataSourceOverrides:
    """
    (Helper Class) DataSourceOverrides class.

    The DataSourceOverrides class is used to establish a context where VirtualDataSources will be overridden.
    """

    def __init__(self, overrides: Dict[str, Union[VirtualDataSource, DataFrame]]):
        """
        Instantiates a new DataSourceOverride.

        :param overrides: A dictionary mapping names of VirtualDataSources to be overridden to DataFrames or data sources overrides.

        :return: A DataSourceOverride class instance.
        """
        from tecton.tecton_context import TectonContext

        self.override_dataframes = {}
        for vds_name, override in overrides.items():
            if isinstance(override, VirtualDataSource):
                self.override_dataframes[vds_name] = override.dataframe()
            elif isinstance(override, DataFrame):
                self.override_dataframes[vds_name] = override
            else:
                raise errors.OVERRIDE_INVALID_TYPE(
                    type(override).__name__, [x.__name__ for x in (VALID_DATA_SOURCE_TYPES + VALID_DATA_FRAME_TYPES)]
                )

        self._validate()
        self.tc = TectonContext.get_instance()

    def __enter__(self):
        self.tc._set_datasource_overrides(self.override_dataframes)

    def __exit__(self, type, value, traceback):
        self.tc._set_datasource_overrides({})

    def _validate(self):
        all_vds = VirtualDataSource.list()
        for vds in self.override_dataframes:
            if vds not in all_vds:
                raise errors.OVERRIDE_VDS_NOT_VALID(vds, all_vds)
