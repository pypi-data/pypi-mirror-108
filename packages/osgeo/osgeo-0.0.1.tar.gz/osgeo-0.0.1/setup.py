from setuptools import setup
from setuptools.command.install import install

name = 'osgeo'
real_name = 'gdal'

description = f'A dummy placeholder for the `{real_name}` package'
error_msg = f'In order to be able to run `from {name} import {real_name}`, \n' \
            f'You were probably trying to install `{real_name}` by running `pip install {name}`.\n' \
            f'Instead, you should either `pip install {real_name}` ' \
            f'or replace `{name}` with `{real_name}` in your requirements.'

readme = f"""
{name} package
===============
{description}

{error_msg}

This package was made so an attacker would not be able to take advantage of this confusion.
"""
readme_type = 'text/x-rst'


class PostInstallCommand(install):
    def run(self):
        raise Exception(error_msg)


cmdclass = dict(install=PostInstallCommand)

setup(
    name=name,
    description=description,
    long_description=readme,
    license="MIT",
    long_description_content_type=readme_type,
    version='0.0.1',
    cmdclass=cmdclass,
)
