#!/usr/bin/env python3.7
from database import DatabaseAccess
from pathlib import Path

import re
import pandas as pd
import argparse

class PandasParserCli:
    """
    Gets the path of csv files and
    converts them into pandas df.
    Only run once.
    """
    def __init__(self, path, multiple_files=True):
        self.path = path
        self.multiple_files = multiple_files

    def _get_csv_paths(self):
        return [filename for filename in Path(self.path).rglob('*.csv')]


    def _convert_csv_files(self):
        if self.multiple_files:
            paths = self._get_csv_paths()
        else:
            paths = [self.path]
        li = []

        for filename in paths:
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)

        frame = pd.concat(li, axis=0, ignore_index=True)
        return frame

    def parse(self):
        df = self._convert_csv_files()
        df.to_csv('/opt/coursepicker/grade-data/combined.csv')


class MigrationCli:
    """
    Not scalable with data bytes (Because of memory limitations)
    """
    def __init__(self, path):
        self.db_access = DatabaseAccess()
        self.path = path

    def init_session(self):
        self.db_access.init_session()

    def _write_to_db(self):
        """
        Writes everything in self.path csv file to database
        :return:
        """

    def migrate(self):
        self.init_session()
        self._write_to_db()
        # print(df)
        df.to_csv('/opt/coursepicker/grade-data/combined.csv')

if __name__ == '__main__':
    cli = MigrationCli(path='/opt/coursepicker/grade-data/combined.csv')
    cli.migrate()
