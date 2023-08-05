import pytest
import json
from delta_lake import const

class TestSilver:
    pass

    def test_create_json_columns_pass(self):
        self.delta_lake.create_json_columns_pass()
        assert self.delta_lake.json_load_insert_values == json.loads(const.json_colum_test)