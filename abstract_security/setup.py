from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_security',
    version='0.0.2',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='abstract_security is a python module that simplifies the handling of environment variables. It provides functions for searching for and reading .env files, checking for the existence of .env files in a specified path, safely loading .env files, and retrieving the value of specified environment variables. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_essentials/abstract_security',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=['abstract_utilities>=0.0.15','python-dotenv>=0.19.2'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    setup_requires=['wheel'],
)
