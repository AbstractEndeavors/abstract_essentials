from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_audio',
    version='0.0.0.3',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='This module provides functionalities to capture and manipulate audio input from a microphone and save them into a text file. It uses an abstract GUI to display the state of audio recording and playback..',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_audio',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=['abstract_utilities>=0.0.1740', 'pydub>=0.25.1', 'abstract_gui>=0.0.53.5','SpeechRecognition>=3.10.0'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    setup_requires=['wheel'],
)
