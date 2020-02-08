from coursepicker.database.migration import MigrationCli

import unittest


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.migration_cli = MigrationCli()

    # Returns True or False.
    def test_get_csv_paths(self):
        paths = self.migration_cli._get_csv_paths('..')
        assert len(paths) == 1
        assert paths == ['utils/testme.csv']


if __name__ == '__main__':
    unittest.main()
