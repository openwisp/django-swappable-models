import os
import sys
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
The unofficial Django swappable models API.
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Attempt to run pandoc on markdown file
    import subprocess
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        ))
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()

setup(
    name='swapper',
    version='0.2.2',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://github.com/wq/django-swappable-models',
    license='MIT',
    packages=['swapper'],
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    classifiers=[
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=['django>=1.6'],
    test_suite='tests',
)
