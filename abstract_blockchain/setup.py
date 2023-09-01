from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_images',
    version='0.0.0.5',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description="This module, part of the `abstract_essentials` package, provides a collection of utility functions for working with images and PDFs, including loading and saving images, extracting text from images, capturing screenshots, processing PDFs, and more.",
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
    install_requires=['abstract_webtools>=0.1.0', 'pyscreenshot>=3.1', 'pdf2image>=1.16.3', 'pytesseract>=0.3.10', 'requests>=2.28.1', 'numpy>=1.25.2', 'abstract_utilities>=0.1.8', 'PyPDF2>=3.0.1', 'abstract_gui>=0.0.55.6'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    # Add this line to include wheel format in your distribution
    setup_requires=['wheel'],
)
