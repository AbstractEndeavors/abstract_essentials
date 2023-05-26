from setuptools import setup, find_packages

setup(
    name='abstract_utilities',
    version='0.0.1',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='abstract_utilities is a collection of utility modules providing a variety of functions to aid in tasks such as data comparison, list manipulation, JSON handling, string manipulation, mathematical computations, and time operations. ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/abstract_endeavors/abstract_utilities',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.11',
    install_requires=[
        # Add your project's requirements here, e.g.,
        # 'numpy>=1.22.0',
        # 'pandas>=1.3.0',
    ],
)
