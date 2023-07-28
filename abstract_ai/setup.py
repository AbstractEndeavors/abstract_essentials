from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
      name='abstract_ai',
      version='0.1.1',
      author='putkoff',
      author_email='partners@abstractendeavors.com',
      description="abstract_ai is a Python module that provides a wide range of functionalities aimed at facilitating and enhancing interactions with AI. Developed by putkoff, it comprises several utility modules to help handle API responses, generate requests, manage tokenization, and deal with other related aspects.",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.11',
      ],
      install_requires=['abstract_gui>=0.0.5',
                        'abstract_utilities>=0.0.151',
                        'abstract_security>=0.0.1',
                        'nltk>=3.6.3',
                        'openai>=0.27.0'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
      

    )
