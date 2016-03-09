"""
    Collection of helpful functions that can be used across the application.
"""
from flask import jsonify, g
import config
import time
import wrappers
import re

# Checking if server is renning in the test environment
TEST_ENV = getattr(config, 'TEST_ENV', False)

def respond(response, http_status=200):
    response['response_timestamp'] = get_timestamp()
    if TEST_ENV:
        response['environment'] = 'testing'

    if 'http_status' in response:
        http_status = response['http_status']
        del response['http_status']

    g.request_end_time = get_timestamp()
    response['request_timestamp'] = g.request_start_time
    response['processing_time'] = g.processing_time()
    response['response_timestamp'] = g.request_end_time
    return jsonify(response), http_status

"""
    Tiny lambda give the current timestamp, needs no arguments.
"""
get_timestamp = lambda: int(time.time())

def enumerate_table(table_name, filter_params = {}):
    """
        Check all existing IDs in a given table
    """

    if not re.match('^[a-zA-Z0-9_]+$', table_name):
        raise Exception('Invalid table name!')

    variables = {'table_name' : table_name}
    where_clause = ''
    if filter_params != {}:
        where_clause = ' WHERE '

        ctr = 0
        for item in filter_params:
            variables[item] = filter_params[item]
            ctr += 1
            where_clause += item + '=:' + item
            if len(filter_params) - ctr > 0:
                where_clause += ' AND '

    db = wrappers.SQLite.init()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM ' + table_name + where_clause, variables)
    ids = cursor.fetchall()
    db.close()

    return map(lambda x: x[0], ids)
