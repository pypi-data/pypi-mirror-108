import pytest
from delta_lake.Bronze import Bronze
from delta_lake.Util import Util


class TestBronze:

    def __init__(self, spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                 storage_silver, input_data_param_v1, input_data_param_v2, input_data_param_v3, mount_data_param,
                 colums_validate_merge_param, new_name, database, target, origin, colum_filter, value_filter,
                 colum_validate_data, value_validate_data, number_items_valide_v1, number_items_valide_v2):
        self.spark = spark
        self.util = Util()
        self.colum_filter = colum_filter
        self.value_filter = value_filter
        self.colum_validate_data = colum_validate_data
        self.value_validate_data = value_validate_data
        self.number_items_valide_v1 = number_items_valide_v1
        self.number_items_valide_v2 = number_items_valide_v2
        self.delta_lake_v1 = Bronze(self.spark, storage_account_name, storage_account_access_key, storage_landing,
                                    storage_bronze, storage_silver, input_data_param_v1, mount_data_param,
                                    colums_validate_merge_param, new_name, database, target, origin)
        self.delta_lake_v2 = Bronze(self.spark, storage_account_name, storage_account_access_key, storage_landing,
                                    storage_bronze, storage_silver, input_data_param_v2, mount_data_param,
                                    colums_validate_merge_param, new_name, database, target, origin)
        self.delta_lake_v3 = Bronze(self.spark, storage_account_name, storage_account_access_key, storage_landing,
                                    storage_bronze, storage_silver, input_data_param_v3, mount_data_param,
                                    colums_validate_merge_param, new_name, database, target, origin)

    def load_data_v1(self):
        self.delta_lake_v1.initialize_config_storage()
        self.delta_lake_v1.validate_tables()
        self.delta_lake_v1.create_colums_merge()
        self.delta_lake_v1.load_data_csv(self.delta_lake_v1.input_data)
        self.delta_lake_v1.merge()
        df = self.delta_lake_v1.spark.sql("select * from {0}.{1}".format(self.delta_lake_v1.database,
                                                                         self.delta_lake_v1.table_name))
        assert df.count() == self.number_items_valide_v1

    def load_data_v2(self):
        self.delta_lake_v2.initialize_config_storage()
        self.delta_lake_v2.validate_tables()
        self.delta_lake_v2.create_colums_merge()
        self.delta_lake_v2.load_data_csv(self.delta_lake_v2.input_data)
        self.delta_lake_v2.initialize_config_storage()
        self.delta_lake_v2.merge()
        df = self.delta_lake_v2.spark.sql("select * from {0}.{1}".format(self.delta_lake_v1.database,
                                                                         self.delta_lake_v1.table_name))
        assert df.count() == self.number_items_valide_v2

    def load_data_v3(self):
        self.delta_lake_v3.initialize_config_storage()
        self.delta_lake_v3.validate_tables()
        self.delta_lake_v3.create_colums_merge()
        self.delta_lake_v3.load_data_csv(self.delta_lake_v3.input_data)
        self.delta_lake_v3.initialize_config_storage()
        self.delta_lake_v3.merge()
        df = self.delta_lake_v3.spark.sql("select {0} From {1}.{2} where {3}={4}".format(self.colum_validate_data,
                                                                                         self.delta_lake_v1.database,
                                                                                         self.delta_lake_v1.table_name,
                                                                                         self.colum_filter,
                                                                                         self.value_filter))
        value = df.collect()
        assert value[0][self.colum_validate_data] == self.value_validate_data

    def initializar_test(self):
        self.delta_lake_v1.spark.sql("DROP TABLE {0}.{1}".format(self.delta_lake_v1.database,
                                                                 self.delta_lake_v1.table_name))
        list_file = self.util.list_folder_delta_lake(self.delta_lake_v1.mount_data)
        for item in list_file:
            self.util.delete_file_delta_lake(item.path)
