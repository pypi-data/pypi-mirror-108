import os
from setuptools import setup
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='cordy',
    version='0.1.1',
    packages=[
        'cordy',
        'cordy.auth',
        'cordy.base',
        'cordy.conf',
        'cordy.crud',
        'cordy.db',
        'cordy.http',
        'cordy.management',
        'cordy.middlewares',
        'cordy.resolvers',
        'cordy.templates', 'cordy.templates.crud', 'cordy.templates.crud.fields',
        'cordy.testing',
        'cordy.xsrf',
    ],
    include_package_data=True,
    license='MIT + Django Licenses',
    description='Proof of concept Django-like framework using python ecosystem',
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://gitlab.levitnet.be/levit/cordy',
    author='Emmanuelle Delescolle',
    author_email='info@levit.be',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'apispec',
        'Beaker',
        'click',
        'cached-property',
        'coloredlogs',
        'gevent',
        'Jinja2',
        'log-symbols',
        'marshmallow',
        'marshmallow-jsonschema',
        'Marshmallow-Peewee',
        'peewee',
        'peewee-migrate',
        'redis',
        'Routes',
        'simple-settings',
        'static',
        'uWSGI',
        'webargs',
        'WebOb',
    ]
)
