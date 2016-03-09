'''
    Utility module to initialize database connection
'''

import sqlite3
import config

def init():
    connection = sqlite3.connect(config.DATABASE_LOC)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    connection.commit()
    return connection

def get_update_params(args_list):
    def per_arg(arg):
        return arg + '=:' + arg
    return ', '.join([per_arg(arg) for arg in args_list])
