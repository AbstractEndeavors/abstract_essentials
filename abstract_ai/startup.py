from setuptools import setup, find_packages

    setup(name='abstract_ai',
      version='0.0.1',
      author='putkoff',
      author_email='partners@abstractendeavors.com',
      description='abstract_ai is a collection of utility modules providing a variety of functions.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/abstract_endeavors/abstract_ai',
      packages=find_packages(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.11',
      ],
      python_requires='>=3.11',
      install_requires=
      ['nltk.tokenize', 'PySimpleGUI', 'openai']
      ,
      entry_points={
          'console_scripts': [
              'abstract_ai=abstract_ai.main:main',
          ],
      }
    )
     