"""
Flask-HoneyAuth
--------------

HTTP authentication module for Flask with honeypot routing support.
"""
import re
from setuptools import setup

with open('flask_honeyauth.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setup(
    name='Flask-HoneyAuth',
    version=version,
    url='http://github.com/prhiggins/flask-honeyauth',
    license='MIT',
    author='Patrick Higgins',
    author_email='phiggin5@uoregon.edu',
    description='HTTP authentication module for Flask with honeypot routing support.',
    py_modules=['flask_honeyauth'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    test_suite="tests",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
