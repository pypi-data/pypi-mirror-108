from setuptools import setup, find_packages

VERSION = '2.64'
DESCRIPTION = 'A python module that makes your text colorful, inspired py termcolor & colorama'
LONG_DESCRIPTION = 'A simple module to make your text colorful easily, using a hex digit & any color. Only for linux'

setup(
	name='colorhex',
	version=VERSION,
	author='dev64',
	author_email='lazarecobani@gmail.com',
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	packages=find_packages(),
	install_requires=[],
	keywords=['colored', 'hex', 'python color', 'colored text', 'linux', 'color'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3.5',
		'Operating System :: Unix',
		'Topic :: Text Processing :: Fonts',
		'Environment :: Console'
	]
)