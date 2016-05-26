"""
Module to load, store, and modifying user preferences.
"""
import ConfigParser
import os

import assetbox.base.helpers as helpers


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
            str: path to the settings config.
        """
        config_dir = os.path.dirname(__file__)
        # Get the parent folder.
        config_dir = os.path.realpath(os.path.join(config_dir, '../../'))

        cfg_files = helpers.get_files(config_dir, '*.cfg')

        if cfg_files:
            for configfile in cfg_files:
                if 'settings.cfg' in configfile:
                    return configfile

        # Write the new config file.
        with open('{0}/settings.cfg'.format(config_dir), 'wb') as configfile:
            self.config.write(configfile)

        return configfile

    def load_config(self):
        """
        Loads a config file, gets the path from get_config.

        Returns:
            ConfigParser: the parser class.
        """
        self.config.read(self.get_config())
        return self.config

    def save_config(self):
        """
        Saves a config file, gets the path from get_config.

        Args:
            ConfigParser: the parser class.
        """
        with open(self.get_config(), 'wb') as configfile:
            self.config.write(configfile)

        return self.config
