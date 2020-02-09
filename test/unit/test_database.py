from coursepicker.database.migration import PandasParserCli
from pathlib import Path

import unittest


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.migration_cli = PandasParserCli('/opt/coursepicker/test/unit/utils')

    # Returns True or False.
    def test_get_csv_paths(self):
        paths = self.migration_cli._get_csv_paths()
        assert len(paths) == 1
        assert paths == [Path('/opt/coursepicker/test/unit/utils/testme.csv')]


if __name__ == '__main__':
    unittest.main()
