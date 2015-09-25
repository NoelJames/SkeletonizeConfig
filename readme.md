A method to use to keep sensitive information out of my git repositories is as follows:

First, add `local.settings.ini` to `.gitignore`

Next, in the config settings of the project use something like the following. 

```python

#Load 'local.settings.ini' from the base directory and assign the sensitive information to config values.

from configparser import ConfigParser
local_settings_ini = os.path.join(BASE_DIR, 'local.settings.ini')
config = ConfigParser()
config.read(local_settings_ini)

SECRET_KEY = config.get('secrets', 'key')

``` 

Because `local.settings.ini` is ignored on commits i know I'll never upload that secrets key. But, when the project is fired up for the first time (or requires new settings) the settings file and values are missing. It's a little cumbersome to go into the project settings to solve the sections and values in the ini file. 


SkeletonizeConfig reads the file with the configuration settings in it and creates a skeleton local.settings.ini file.


## Usages
```
usage: skeletonize_config  [-h] [-i INI_FILE] [-o] [-r] source_file

localize settings from python config

positional arguments:
  source_file           python file which parses the ini

optional arguments:
  -h, --help            show this help message and exit
  -i INI_FILE, --ini_file INI_FILE
                        ini file to save to. Default: ./local.settings.ini
  -o, --overwrite       overwrite existing ini_file
  -r, --remove_missing  remove old values in existing ini_file

```

## Example

```
$ python skeletonize_config.py  ../tests/scripts/settings.py 
DEBUG:root:arguments: Namespace(ini_file='local.settings.ini', overwrite=False, remove_missing=False, source_file='../tests/scripts/settings.py')
DEBUG:root:Loaded: ../tests/scripts/settings.py to <_frozen_importlib.SourceFileLoader object at 0x101220710>
DEBUG:root:Config sections found ['debug', 'server', 'database', 'foo', 'email', 'secrets']
DEBUG:root:Adding section [debug]
DEBUG:root:Adding section [debug] name "internal_ips"
DEBUG:root:Adding section [debug] name "debug"
DEBUG:root:Adding section [server]
DEBUG:root:Adding section [server] name "base_url"
DEBUG:root:Adding section [database]
DEBUG:root:Adding section [database] name "port"
DEBUG:root:Adding section [database] name "user"
DEBUG:root:Adding section [database] name "name"
DEBUG:root:Adding section [database] name "password"
DEBUG:root:Adding section [database] name "host"
DEBUG:root:Adding section [database] name "engine"
DEBUG:root:Adding section [foo]
DEBUG:root:Adding section [foo] name "int_name"
DEBUG:root:Adding section [foo] name "float_name"
DEBUG:root:Adding section [email]
DEBUG:root:Adding section [email] name "port"
DEBUG:root:Adding section [email] name "user"
DEBUG:root:Adding section [email] name "password"
DEBUG:root:Adding section [email] name "host"
DEBUG:root:Adding section [email] name "default_from"
DEBUG:root:Adding section [email] name "use_tls"
DEBUG:root:Adding section [secrets]
DEBUG:root:Adding section [secrets] name "key"
Success: local.settings.ini

```

## Install

```
git clone https://github.com/NoelJames/SkeletonizeConfig.git
cd SkeletonizeConfig
python setup.py install
```


Check for updates at [Github.com/NoelJames/SkeletonizeConfig](https://github.com/NoelJames/SkeletonizeConfig)

