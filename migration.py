#!/usr/bin/env python3.7
from coursepicker.database.database import DatabaseAccess, Grade
from pathlib import Path
from coursepicker.utils.config import get_config
import logging

import pandas as pd

# TODO make configurable (argparse)
ENV = 'prod'
logger = logging.getLogger('migration')


class PandasParserCli:
    """
    Gets the path of csv files and
    converts them into pandas df.
    Only run once.
    """
    def __init__(self, path):
        self.path = path

    def _get_csv_paths(self):
        return [filename for filename in Path(self.path).rglob('*.csv')]

    def _convert_csv_files(self):
        paths = self._get_csv_paths()
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
        self.config = get_config(ENV)
        self.db_access = DatabaseAccess(self.config)
        self.path = path

    def normalize(self, string):
        return string.replace(' ', '-').lower()

    def init_session(self):
        self.db_access.init_session()

    def _write_to_db(self):
        """
        Writes all grade entries in self.path csv file to database
        :return:
        """
        df = pd.read_csv(self.path, index_col=None, header=0)
        for index, row in df.iterrows():
            fields = {
                'campus': row['Campus'],
                'year': row['Year'],
                'session': row['Session'],
                'subject': row['Subject'],
                'code': row['Course'],
                'detail': row['Detail'],
                'section': row['Section'],
                'title': row['Title'],
                'professor': self.normalize(str(row['Professor'])),
                'enrolled': row['Enrolled'],
                'avg': row['Avg'],
                'std_dev': row['Std'],
                'high': row['High'],
                'low': row['Low'],
            }
            grade_entry = Grade(**fields)
            self.db_access.add_object(grade_entry)
        self.db_access.session.commit()

    def migrate(self):
        self.init_session()
        self._write_to_db()
        # print(df)


if __name__ == '__main__':
    cli = MigrationCli(path='/opt/coursepicker/grade-data/combined.csv')
    cli.migrate()
