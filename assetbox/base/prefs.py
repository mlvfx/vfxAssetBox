"""
Module to load, store, and modifying user preferences.
"""
import ConfigParser
import logging
import os

import assetbox.base.helpers as helpers

LOGGER = logging.getLogger(__name__)


class PreferenceHelper(object):
    """
    Helper class to manage preferences.
    """
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.add_section('project')
        self.config.add_section('ui')

    def get_config(self):
        """
        If a config does not exist, create one, otherwise return it.

        Returns:
            str: Path to the settings config.
        """
        config_dir = os.path.dirname(__file__)
        # Get the parent folder.
        config_dir = os.path.realpath(os.path.join(config_dir, '../../'))

        cfg_files = helpers.get_files(config_dir, '*.cfg')

        if cfg_files:
            for config_file in cfg_files:
                if 'settings.cfg' in config_file:
                    return config_file

        # Write the new config file.
        config_file = '{0}/settings.cfg'.format(config_dir)
        with open(config_file, 'wb') as config_path:
            self.config.write(config_path)

        return config_file

    def load_config(self):
        """
        Loads a config file, gets the path from get_config.

        Returns:
            ConfigParser: the parser class.
        """
        config_file = self.get_config()
        self.config.read(config_file)
        return self.config

    def save_config(self):
        """
        Saves a config file, gets the path from get_config.

        Args:
            ConfigParser: The parser class.
        """
        config_file = self.get_config()
        with open(config_file, 'wb') as configfile:
            self.config.write(configfile)

        return configfile

    def get_attr(self, group, attr):
        """
        Return an attribute related to the project.

        Args:
            group (str): The group of attributes.
            attr (str): The attribute to query.
        """
        if self.config:
            try:
                value = self.config.get(group, attr)
                return value
            except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
                LOGGER.debug('{0} attribute or section not found.'.format(attr))
            else:
                return False

    def set_attr(self, group, attr, value):
        """
        Set an attribute related to the project.

        Args:
            group (str): The group of attributes.
            attr (str): The attribute to set.
            value (str): The value to set.
        """
        if self.config:
            self.config.set(group, attr, value)
            configfile = self.save_config()
            LOGGER.info('Saved config to: {0}'.format(configfile))
