from delta_lake.DataLake import DataLake
from delta.tables import DeltaTable


class Silver(DataLake):

    def __init__(self, spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                 storage_silver, input_data_param, mount_data_param, colums_validate_merge_param, new_name, database,
                 target, origin, colums_silver):
        self.colums_silver = colums_silver
        super().__init__(spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                         storage_silver, input_data_param, mount_data_param, colums_validate_merge_param, new_name,
                         database, target, origin)
        self.initialize_variables()

    def merge(self):
        try:
            if self.table_exist:
                deltaTable = DeltaTable.forPath(self.spark, self.mount_data)
                deltaTable.alias(self.target) \
                    .merge(self.events.alias(self.origin), self.string_validate_columns) \
                    .whenMatchedUpdate(set=self.json_load_insert_values) \
                    .whenNotMatchedInsert(values=self.json_load_insert_values) \
                    .execute()
            else:
                self.events.write.format("delta").save(self.mount_data)
                self.spark.sql("CREATE TABLE IF NOT EXISTS {0}.{1} USING DELTA LOCATION '{2}'".format(self.database,
                                                                                                      self.table_name,
                                                                                                      self.mount_data))
        except Exception as e:
            print("Error update or create table: " + self.table_name + " explain: " + str(e))

    def initialize_variables(self):
        self.input_data = "{0}{1}".format(self.storage_bronze, self.mount_data_param)
        self.mount_data = "{0}{1}".format(self.storage_silver, self.mount_data_param)
        self.colums_validate_merge = self.colums_validate_merge_param.split(',')
        self.colums_silver_array = self.colums_silver.split(',')

    def load_data(self, input_data):
        self.events = self.spark.read.format("delta").load("{0}".format(input_data))

    def create_json_columns_pass(self):
        insert_values = "{"
        for item in self.colums_silver_array:
            if item is not "":
                insert_values = "{0}{1}".format(insert_values, '"{0}":"{1}.{0}", '.format(item, self.origin))

        insert_values = insert_values[0: len(insert_values) - 2] + '}'

        self.json_load_insert_values = json.loads(insert_values)
        print(self.json_load_insert_values)