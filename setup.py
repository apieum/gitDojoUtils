# -*- coding: utf8 -*-
from setuptools import setup, find_packages
import os

pkgName = 'gitDojoUtils'
setup(
    name=pkgName,
    version='0.1',
    url='http://www.python.org/pypi/' + pkgName,
    author='Grégory Salvan',
    author_email='apieum@gmail.com',
    license='LGPL',
    description='Utils for coding dojo',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages('.'),
    package_dir={'gitDojoUtils': 'gitDojoUtils'},
    namespace_packages=['gitDojoUtils'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['gitDojo = gitDojoUtils.bin.gitDojo:GitDojo']
    },
    install_requires=['setuptools'],
)
