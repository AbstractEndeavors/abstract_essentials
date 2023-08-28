from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_utilities',
    version='0.1.8',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='abstract_utilities is a collection of utility modules providing a variety of functions to aid in tasks such as data comparison, list manipulation, JSON handling, string manipulation, mathematical computations, and time operations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_utilities',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.11',
    ],
    install_requires=['pexpect>=4.8.0', 'abstract_security>=0.0.1'],
   package_dir={"": "src"},
   packages=setuptools.find_packages(where="src"),
   python_requires=">=3.6",
  

)
