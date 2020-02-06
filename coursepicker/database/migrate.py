#!/usr/bin/env python3.7
from coursepicker.database.database import DatabaseAccess
from os import walk

class MigrationCli:
    def __init__(self):
        self.db_access = DatabaseAccess()
        self.db_access.init_session()


    def _read_csv_files(self, path):
        for (dirpath, dirnames, filenames) in walk(path):
            pass  # TODO

    def migrate(self):
        file = self._read_csv_files('../../grade-data/tableau_dashboard/UBCV')


if __name__ == '__main__':
    cli = MigrationCli()
    cli.migrate()
