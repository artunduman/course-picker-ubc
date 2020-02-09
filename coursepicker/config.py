# TODO
import configparser

def get_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config