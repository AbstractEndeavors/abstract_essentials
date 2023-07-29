from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_webtools',
    version='0.0.1',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='Abstract Web Tools is a Python package that provides various utility functions for web scraping tasks. It is built on top of popular libraries such as `requests`, `BeautifulSoup`, and `urllib3` to simplify the process of fetching and parsing web content.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_webtools',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'beautifulsoup4>=4.9.0',
        'requests>=2.25.0',
        'urllib3>=1.26.0',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
