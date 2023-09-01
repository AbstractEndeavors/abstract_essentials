from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_blockchain',
    version='0.0.0.0',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description="i just wanna wear my clown suit on the outside and have my business suit on underneath. and if thats not how you feel, you're probably NGMI. feel free to contribute.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.11',
      ],
    install_requires=[],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    # Add this line to include wheel format in your distribution
    setup_requires=['wheel'],
)
