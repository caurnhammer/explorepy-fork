#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function
)

import io
import os
import re
import sys
from glob import glob
from os.path import (
    basename,
    dirname,
    join,
    splitext
)

from setuptools import (
    Extension,
    find_packages,
    setup
)


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


my_req = ['numpy',
          'scipy',
          'pyedflib',
          'click==7.1.2',
          'appdirs==1.4.3',
          'sentry_sdk==1.19.1',
          'mne',
          'eeglabio',
          'pandas',
          'pyserial',
          'pyyaml']  # noqa: E501
test_requirements = ["pytest==6.2.5",
                     "pytest-mock==3.10.0",
                     "pytest-html==3.2.0",
                     "flake8==4.0.1",
                     "isort==5.10.1"]
extras = {"test": test_requirements}

ext_modules_list = []
current_platform = sys.platform

if not os.environ.get('READTHEDOCS'):
    my_req.append('pylsl')
    libPath = "lib"
    if current_platform == 'win32' or current_platform == 'win64':
        windows_lib_path = os.path.join(libPath, 'windows')
        ext_modules_list.append(Extension(
            name='explorepy._exploresdk',
            sources=[os.path.join(windows_lib_path, 'swig_interface_wrap.cxx'),
                     os.path.join(windows_lib_path, 'BluetoothHelpers.cpp'),
                     os.path.join(windows_lib_path, 'DeviceINQ.cpp'),
                     os.path.join(windows_lib_path, 'BTSerialPortBinding.cpp')],
            swig_opts=['-c++']
        ))

    elif current_platform.startswith('linux'):
        linux_lib_path = os.path.join(libPath, 'linux')

        ext_modules_list.append(Extension(
            name='explorepy._exploresdk',
            sources=[os.path.join(linux_lib_path, 'swig_interface_wrap.cxx'),
                     os.path.join(linux_lib_path, 'DeviceINQ.cpp'),
                     os.path.join(linux_lib_path, 'BTSerialPortBinding.cpp')],
            extra_link_args=["-lbluetooth"],
            swig_opts=['-c++']
        ))
setup(
    name='explorepy',
    version='2.0.0',
    license='MIT license',
    description='Python API for Mentalab biosignal aquisition devices',
    long_description_content_type="text/markdown",
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Mentalab GmbH.',
    author_email='mohamad.atayi@mentalab.com',
    url='https://github.com/Mentalab-hub/explorepy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    ext_modules=ext_modules_list,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    keywords=[
        'Mentalab', 'Explorepy', 'EEG signal',
    ],
    install_requires=my_req,
    extras_require=extras,
    entry_points='''
        [console_scripts]
        explorepy=explorepy.cli:cli
    ''',
)
