import configparser


def get_config(env):
    if env != 'prod' or 'local':
        env = 'local'

    config = configparser.ConfigParser()
    config.read('../conf/{}.ini'.format(env))
    db_config = config['database']
    config['DATABASE_URL'] = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        db_config['user'],
        db_config['password'],
        db_config['host'],
        db_config['db_identifier']
    )