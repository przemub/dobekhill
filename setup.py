try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Dobek Hill',
    'author': 'przemub',
    'url': 'https://1mi.pl/~przemub/dobekhill',
    'download_url': 'https://1mi.pl/~przemub/dobekhill',
    'author_email': 'przemub@przemub.pl',
    'version': '0.1',
    'install_requires': [],
    'packages': ['dobekhill'],
    'scripts': [],
    'name': 'dobekhill'
}

setup(**config, install_requires=['termcolor'])

