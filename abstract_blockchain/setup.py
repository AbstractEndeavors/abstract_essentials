from time import time
import setuptools
from setuptools import setup, find_packages

with open('README.md', "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='abstract_blockchain',
    version='0.0.0.77',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='The Abstract Blockchain package provides a collection of modules designed to simplify interaction with blockchain networks, smart contracts, and related components. It offers tools for managing RPC parameters, working with smart contract ABIs, and facilitating user-friendly interactions through graphical user interfaces (GUIs).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_blockchain',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Intended Audience :: Financial and Insurance Industry'
    ],
    keywords='database, automation, API, testing, cryptography',  # This is how you add keywords
    install_requires=[
        'PySimpleGUI>=4.60.5', 'setuptools>=66.1.1', 'abstract_security>=0.0.1', 'abstract_webtools>=0.1.0', 'abstract_gui>=0.0.53.5', 'web3>=6.9.0', 'abstract_utilities>=0.2.0.52', 'requests>=2.31.0', 'hexbytes>=0.3.1'
    ],
    package_dir={"": "src"},
    package_data={'data': ['rpc_list.json']},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    setup_requires=['wheel'],
)
