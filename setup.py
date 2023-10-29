from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_ai',
    version='0.1.7.42',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description="abstract_ai is a Python module that serves as a bridge between your application and the OpenAI GPT-3 API. It provides a convenient interface for sending requests, managing responses, and controlling the behavior of the API calls. This module is highly customizable, allowing you to establish prompts, instructions, and response handling logic.",
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
    install_requires=['abstract_security>=0.0.1', 'abstract_webtools>=0.1.4.90', 'tiktoken>=0.5.1', 'abstract_utilities>=0.2.2.1', 'abstract_gui>=0.0.60.0', 'pyperclip>=1.8.2', 'openai>=0.28.1', 'requests>=2.31.0', 'nltk>=3.8.1'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    # Add this line to include wheel format in your distribution
    setup_requires=['wheel'],
)
