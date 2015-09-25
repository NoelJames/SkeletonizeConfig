from unittest import TestCase
from collections import OrderedDict

from skeletonize_config import skeletonize_config

ini_contents = """
[server]
base_url = http://127.0.0.1:8000

[database]
engine: example_engine
name: database_name
user: username
password: password
host: 127.0.0.1
port: 666

[debug]
debug: true
internal_ips: 127.0.0.1

[old_section]
foo: bar
oh: mt
"""


class TestParser(TestCase):
    def setUp(self):
        open('local.settings.ini', 'w').write(ini_contents)

    def test_argument_help(self):
        args = skeletonize_config.parse_arguments('some_file.py')
        self.assertEquals(args.ini_file, 'local.settings.ini')
        self.assertEquals(args.source_file, 'some_file.py')

        args = skeletonize_config.parse_arguments('some_file.py', '-i', 'foo.ini')
        self.assertEquals(args.ini_file, 'foo.ini')
        self.assertEquals(args.source_file, 'some_file.py')
        self.assertFalse(args.remove_missing)
        self.assertFalse(args.overwrite)

        args = skeletonize_config.parse_arguments('some_file.py', '--ini_file', 'foo.ini', '-r', '-o')
        self.assertEquals(args.ini_file, 'foo.ini')
        self.assertEquals(args.source_file, 'some_file.py')
        self.assertTrue(args.remove_missing)
        self.assertTrue(args.overwrite)

    def test_load_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as context:
            skeletonize_config.find_configuration('some_file.py')
        self.assertTrue('some_file.py' in str(context.exception))

    def test_load_example(self):
        expect = {
            'server': {'base_url'},
            'email': {'user', 'password', 'host', 'port', 'default_from', 'use_tls'},
            'secrets': {'key'},
            'foo': {'float_name', 'int_name'},
            'debug': {'internal_ips', 'debug'},
            'database': {'engine', 'name', 'user', 'password', 'host', 'port'}
        }
        configs = skeletonize_config.find_configuration('scripts/settings.py')
        self.assertDictEqual(configs, expect)

    def test_update_config_remove_old(self):
        new_configs = {
            'server': {'base_url', 'backup_url'},
            'debug': {'debug'},
            'database': {'host'},
            'section_new': {'val_new'}
        }
        config = skeletonize_config.update_config(
            new_configs,
            'scripts/local.settings.ini',
            remove_missing=True
        )
        expect = OrderedDict([
            ('server', OrderedDict([
                ('base_url', 'http://127.0.0.1:8000'),
                ('backup_url', '')
            ])),
            ('database', OrderedDict([
                ('host', '127.0.0.1')
            ])),
            ('debug', OrderedDict([
                ('debug', 'true')
            ])),
            ('section_new', OrderedDict([
                ('val_new', '')
            ]))
        ])

        self.assertEquals(config._sections, expect)

    def test_update_config_keep_old(self):
        new_configs = {
            'server': {'base_url', 'backup_url'},
            'debug': {'debug'},
            'database': {'host'},
            'section_new': {'val_new'}
        }
        config = skeletonize_config.update_config(
            new_configs,
            'scripts/local.settings.ini',
            remove_missing=False
        )
        expect = OrderedDict([
            ('server', OrderedDict([
                ('base_url', 'http://127.0.0.1:8000'),
                ('backup_url', '')
            ])),
            ('database', OrderedDict([
                ('engine', 'example_engine'),
                ('name', 'database_name'),
                ('user', 'username'),
                ('password', 'password'),
                ('host', '127.0.0.1'),
                ('port', '666')
            ])),
            ('debug', OrderedDict([
                ('debug', 'true'),
                ('internal_ips', '127.0.0.1')
            ])),
            ('old_section', OrderedDict([
                ('foo', 'bar'),
                ('oh', 'mt')
            ])),
            ('section_new', OrderedDict([('val_new', '')])),
        ])

        self.assertEquals(config._sections, expect)
