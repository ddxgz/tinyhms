import os

from six.moves import configparser


class Config(object):
    def __init__(self, conf_file=None):
        if conf_file:
            self.config_file = conf_file
            self._get_config(specified=True)
        else:
            self._get_config()

    def _get_config(self, specified=False):
        if specified is True:
            config_file = self.config_file
        else:
            config_file = os.environ.get('',
                                     './configuration')
        config = configparser.SafeConfigParser()
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

conf = Config()
