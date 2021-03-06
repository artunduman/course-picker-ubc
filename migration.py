#!/usr/bin/env python3.7
from coursepicker.database.database import DatabaseAccess, Grade
from pathlib import Path
from coursepicker.utils.config import get_config
import logging
import argparse
import pandas as pd

# TODO make configurable (argparse)
logger = logging.getLogger('migration')


def get_args():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(title='Actions',
                                      dest='action',
                                      description='Action',
                                      help='')

    describe = subparser.add_parser('describe')
    migrate = subparser.add_parser('migrate')
    delete = subparser.add_parser('delete')

    describe.add_argument('-e',
                          '--environment',
                          dest='env',
                          required=True,
                          default='local',
                          help='Environment to load config for')

    migrate.add_argument('-e',
                         '--environment',
                         dest='env',
                         required=True,
                         default='local',
                         help='Environment to load config for')

    delete.add_argument('-e',
                         '--environment',
                         dest='env',
                         required=True,
                         default='local',
                         help='Environment to load config for')

    return parser.parse_args()


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
    def __init__(self, path, environment):
        self.config = get_config(environment)
        self.db_access = DatabaseAccess(self.config)
        self.path = path

    def _normalize(self, string):
        return string.replace(' ', '-').lower()

    def init_session(self):
        # import pdb; pdb.set_trace()
        self.db_access.init_session()

    def _write_to_db(self):
        """
        Writes all grade entries in self.path csv file to database
        :return:
        """
        df = pd.read_csv(self.path, index_col=None, header=0)
        grades = []
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
                'professor': self._normalize(str(row['Professor'])),
                'enrolled': row['Enrolled'],
                'avg': row['Avg'],
                'std_dev': row['Std'],
                'high': row['High'],
                'low': row['Low'],
            }
            grade_entry = Grade(**fields)
            grades.append(grade_entry)

        self.db_access.session.bulk_save_objects(grades)
        self.db_access.session.commit()

    def migrate(self):
        self.init_session()
        self._write_to_db()

    def describe_db(self):
        self.init_session()
        for instance in self.db_access.session.query(Grade):
            print('Year {} Subject {} Code {} Prof {}'.format(
                instance.year,
                instance.subject,
                instance.code,
                instance.professor
            ))

    def delete(self):
        self.init_session()
        try:
            num_rows_deleted = self.db_access.session.query(Grade).delete()
            self.db_access.session.commit()
            print('Deleted rows: {}'.format(num_rows_deleted))
        except Exception as e:
            self.db_access.session.rollback()

    def write_averages(self):
        raise NotImplementedError


if __name__ == '__main__':
    args = get_args()
    cli = MigrationCli(path='/opt/coursepicker/grade-data/combined.csv', environment=args.env)
    if args.action == 'describe':
        cli.describe_db()
    if args.action == 'migrate':
        cli.migrate()
    if args.action == 'delete':
        cli.delete()
    if args.action == 'averages':
        cli.write_averages()
