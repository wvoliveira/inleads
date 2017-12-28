#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

"""
Script dedicated to collecting Catho's direct leads from the database
SQL SERVER settings file in /etc/odbc.ini
"""

import ConfigParser
import pypyodbc
import json
import logging
import argparse


def log_define(path_file, loglevel):
    _format = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(filename=path_file, format=_format, level=loglevel)
    return logging


parser = argparse.ArgumentParser(description='Roda procedures com base no arquivo de configuracao .ini')
parser.add_argument('-c', '--config', help='config file', required=True)
args = parser.parse_args()
CONFIG_FILE = args.config


def config_parser(section):
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)

    if config.has_section(section):
        items_dict = dict(config.items(section))
        return items_dict


logger_config = config_parser('logging')
logger = log_define(logger_config['file'], logger_config['level'])
logger.debug('Logger defined')


def db_connection(conf, database, user, password):
    try:
        connection_string = 'DSN={};Database={};UID={};PWD={};'.format(conf, database, user, password)
        connection = pypyodbc.connect(connection_string, timeout=5)
        return connection
    except Exception as error:
        logger.critical(error)
        exit(2)


def db_query(cursor, query):
    rows = cursor.execute(query).fetchall()
    return rows


def main():

    sql_conf = config_parser('sql_conf')
    procedures = config_parser('procedures')
    logger.debug('Loaded configs')

    campaign_info = dict()

    for campaign_name in sorted(procedures):
        command = procedures[campaign_name]

        try:
            logger.debug('Trying {}'.format(campaign_name))

            connection = db_connection(sql_conf['conf'], sql_conf['database'], sql_conf['user'], sql_conf['pass'])
            cursor = connection.cursor()
            cursor.set_timeout(10)
            logger.debug('Connection established')

            result = db_query(cursor, command)
            logger.debug('Result: {}'.format(result))

            connection.close()
        except Exception as error:
            logger.critical(error)
            result = [(-1,), (-1,), (-1,), (-1,)]
            pass

        leads_worked_dif, leads_virgin = result[0][0], result[1][0]
        leads_available, leads_worked_total = result[2][0], result[3][0]

        logger.debug('Leads worked dif: {}; Leads virgin: {}; Leads available {}; Leads worked total: {}'
                     .format(leads_worked_dif, leads_virgin, leads_available, leads_worked_total))

        campaign_info[campaign_name] = {'Catho_Trabalhados_Dif': leads_worked_dif, 'Catho_Virgens': leads_virgin,
                                        'Catho_Disponiveis': leads_available, 'Catho_Trabalhados_Total': leads_worked_total}

    campaign_json = json.dumps(campaign_info, sort_keys=True, separators=(',', ':'))
    logger.debug('In json dumps: {}'.format(campaign_json))

    print(campaign_json)


if __name__ == '__main__':
    main()

