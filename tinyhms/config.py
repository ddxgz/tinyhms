import os
import logging

from six.moves import configparser


# logging.basicConfig(level=logging.DEBUG,
#                 format='[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
#                 datefmt='%d %b %Y %H:%M:%S')


class Config(object):
    def __init__(self, conf_file=None):
        # logging.debug('cwd:{}'.format(os.getcwd()))
        if conf_file:
            self.config_file = conf_file
            self._get_config(specified=True)
        else:
            self._get_config()

    def _get_config(self, specified=False):
        # logging.debug('cwd:{}'.format(os.getcwd()))
        if specified is True:
            config_file = self.config_file
        else:
            config_file = os.environ.get('',
                                     './configuration')
        config = configparser.ConfigParser()
        config.read(config_file)

        if config.has_section('common'):
            #self.mq_host = config.get('common', 'mq_host')
            try:
                self.api_version = config.get('common', 'api_version')
                # self.log_filename = log_filename
            except:
                self.api_version = '1'
            try:
                self.log_filename = config.get('common', 'log_filename')
                # self.log_filename = log_filename
            except:
                self.log_filename = None
            try:
                log_level = config.get('common', 'log_level')
                self.log_level = log_level.upper()
            except:
                self.log_level = None
            try:
                redis_ip = config.get('common', 'redis_ip')
                self.redis_ip = redis_ip
            except:
                self.redis_ip = '127.0.0.1'
        if config.has_section('model'):
            try:
                db_type = config.get('model', 'db_type')
                self.db_type = db_type.lower()
            except:
                self.db_type = 'sqlite3'
            if self.db_type == 'sqlite3':
                try:
                    db_filename = config.get('model', 'db_filename')
                    self.db_filename = db_filename.lower()
                except:
                    self.db_filename = 'hms'
        if config.has_section('swift'):
            try:
                self.auth_version = config.get('swift', 'auth_version')
                # self.log_filename = log_filename
            except:
                self.auth_version = '1'
            try:
                self.auth_host = config.get('swift', 'auth_host')
                # self.log_filename = log_filename
            except:
                self.auth_host = '192.168.59.200'
            try:
                self.auth_port = config.get('swift', 'auth_port')
            except:
                self.auth_port = '8080'
            try:
                account = config.get('swift', 'account')
                username = config.get('swift', 'username')
                self.account_username = account + ':' + username
            except:
                self.account_username = 'test:tester'
            try:
                self.password = config.get('swift', 'password')
            except:
                self.password = 'testing'
            try:
                auth_prefix = config.get('swift', 'auth_prefix')
            except:
                self.auth_prefix = 'auth'

            self.auth_url = ""

            self.auth_url += "http://%s:%s%s" % (self.auth_host, self.auth_port, auth_prefix)
            if self.auth_version == "1":
                self.auth_url += 'v1.0'

            try:
                self.container = config.get('swift', 'container')
            except:
                self.container = 'hms'


conf = Config()
