from setuptools import setup, find_packages

VERSION = '0.1.0'

setup(
    name='SkeletonizeConfig',
    version=VERSION,
    url='https://github.com/NoelJames/SkeletonizeConfig',
    author='Noel James',
    author_email='noel@rescommunes.ca',
    license="MIT",
    packages=['skeletonize_config'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'skeletonize_config = skeletonize_config.skeletonize_config:main',
        ],
    },
)