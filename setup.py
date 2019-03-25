import os
import sys
import codecs
from setuptools import setup

try:
    SETUP_DIRNAME = os.path.dirname(__file__)
except NameError:
    SETUP_DIRNAME = os.path.dirname(sys.argv[0])

if SETUP_DIRNAME:
    os.chdir(SETUP_DIRNAME)


def read(fname):
    """
    Read a file from the directory
    where setup.py is.

    :param fname: filename to read
    :return: text
    """
    file_path = os.path.join(SETUP_DIRNAME, fname)
    with codecs.open(file_path, encoding='utf-8') as rfh:
        return rfh.read()


setup(
    name="sugar-ui",
    version="0.0.0",
    packages=[
        "sugarui",
        "sugarui.windows",
        "sugarui.widgets",
    ],
    url='https://github.com/sugarsack/sugar-ui',
    license='MIT',
    author='Bo Maryniuk',
    author_email='bo@maryniuk.net',
    description='Sugar Text UI for terminals',
    long_description="Sugar Test UI for terminals. This package is a part of Sugarsack project.",
    scripts=[],
    install_requires=[
        "npyscreen",
        "pyyaml",
        "requests",
    ],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
)
