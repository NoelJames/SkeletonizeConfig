"""
The MIT License (MIT)

Copyright (c) 2015 Noel James (noel@rescommunes.ca)


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


source: https://github.com/NoelJames/SkeletonizeConfig
"""


from sys import argv, exit
import argparse
import logging
from importlib import machinery
from unittest.mock import patch
import configparser
import os.path

log = logging.getLogger()


def parse_arguments(*args):
    parser = argparse.ArgumentParser(description='localize settings from python config')
    parser.add_argument('source_file', help="python file which parses the ini")
    parser.add_argument('-i', '--ini_file', help="ini file to save to. Default: ./local.settings.ini ",
                        default='local.settings.ini')
    parser.add_argument('-o', '--overwrite', help="overwrite existing ini_file", action='store_true')
    parser.add_argument('-r', '--remove_missing', help="remove old values in existing ini_file", action='store_true')
    parsed_args = parser.parse_args(args)
    log.debug("arguments: {}".format(repr(parsed_args)))
    return parsed_args


class MockConfigGetType():
    def __init__(self):
        self.configs = {}

    def __call__(self, *args, **kwargs):
        section, value_type, name = args
        if section not in self.configs:
            self.configs[section] = []
        self.configs[section].append(name)
        if value_type is bool:
            return 'false'
        if value_type is int:
            return '1'
        return '0.1'


class MockConfigGet():
    def __init__(self):
        self.configs = {}

    def __call__(self, *args, **kwargs):
        section, name = args
        if section not in self.configs:
            self.configs[section] = []
        self.configs[section].append(name)
        return 'false'


@patch.object(configparser.RawConfigParser, '_get', new_callable=MockConfigGetType)
@patch.object(configparser.RawConfigParser, 'get', new_callable=MockConfigGet)
def find_configuration(source_file, mocked_config, mock_config_typed):
    source = load_source_file(source_file)
    try:
        source.load_module()
    except FileNotFoundError:
        log.debug("unable to load module {}".format(source))
        raise
    configs = mocked_config.configs
    for section, values in mock_config_typed.configs.items():
        if section not in configs:
            configs[section] = []
        configs[section].extend(values)
    log.debug("Config sections found {}".format(list(configs.keys())))

    sorted_configs = {}
    for section in configs:
        sorted_configs[section] = set(configs[section])
    return sorted_configs


def load_source_file(source_file):
    source = machinery.SourceFileLoader('source_file', source_file)
    log.debug("Loaded: {} to {}".format(source_file, source))
    return source


def update_config(new_configs, ini_file, remove_missing=False):
    config = configparser.ConfigParser()
    config.read(ini_file)

    current_sections = set(config.sections())
    new_sections = set(new_configs.keys())

    removed_sections = current_sections - new_sections
    if remove_missing:
        for section in removed_sections:
            log.debug("Removing section [{}]".format(section))
            del config[section]

    exists_sections = new_sections & current_sections
    for section in exists_sections:
        current_variables = set(config[section])
        new_variables = new_configs[section]
        if remove_missing:
            for name in current_variables - new_variables:
                log.debug('Removing section [{}] name "{}"'.format(section, name))
                del config[section][name]

        for name in new_variables - current_variables:
            log.debug('Adding section [{}] name "{}"'.format(section, name))
            config[section][name] = ''

    new_sections = new_sections - current_sections
    for section in new_sections:
        log.debug('Adding section [{}]'.format(section))
        if section not in config:
            config[section] = {}
        for name in new_configs[section]:
            log.debug('Adding section [{}] name "{}"'.format(section, name))
            config[section][name] = ''
    return config


def save_config(config, ini_file, overwrite=False):
    if not overwrite and os.path.exists(ini_file):
        exit("Error: ini_file '{}' exists and overwite is False".format(ini_file))
    with open(ini_file, 'w') as configfile:
        config.write(configfile)


def main():
    logging.basicConfig(level=logging.DEBUG)
    parsed_args = parse_arguments(*argv[1:])
    try:
        new_configs = find_configuration(parsed_args.source_file)
    except FileNotFoundError:
        exit("Error: Unable to load 'source_file' {}".format(parsed_args.source_file))
    config = update_config(
        new_configs,
        parsed_args.ini_file,
        remove_missing=parsed_args.remove_missing
    )
    save_config(
        config,
        parsed_args.ini_file,
        overwrite=parsed_args.overwrite
    )
    print("Success: {}".format(parsed_args.ini_file))


if __name__ == '__main__':
    main()
