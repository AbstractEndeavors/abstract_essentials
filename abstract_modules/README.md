#abstract_modules
# Python Module Upload to PyPI

This utility script allows you to easily upload your Python module to the Python Package Index (PyPI) using Twine. It automates several steps of the packaging and distribution process, making it easier to share your module with the Python community.

## Prerequisites

Before using this script, ensure you have the following prerequisites:

- Python 3.x installed on your system
- `twine`, `build`,`abstract_utilities`,`abstract_gui` and `pexpect` packages installed. You can install them using `pip`:

  ```bash
  pip install twine build pexpect
  ```

## Getting Started

1. Clone the repository or download the script file (`upload_to_pypi.py`) to your local machine.

2. Navigate to the directory where your Python module is located using the command line.

3. **Optional**: If you use a virtual environment, activate it before proceeding.

## Usage

Run the script `upload_to_pypi.py` with Python 3:

```bash
python3 upload_to_pypi.py
```

The script will guide you through the following steps:

1. **Selecting Module Directory**: You will be prompted to pick the module directory using a GUI window. This directory should contain the necessary files, including the `setup.py` file.
![Screenshot from 2023-08-31 02-37-23](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/beaf5c3f-54d3-4565-a562-c209ee7db96a)


2. **Updating Version Number**: If the version number in the `setup.py` file matches an existing version in the `dist` directory, you will be asked to enter a new version number.
![Screenshot from 2023-08-31 02-38-10](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/292e7977-c177-4c87-9448-ede4d041ba84)


3. **Building the Module**: The script will build your module using the `setup.py` script. The distribution files (wheels) will be placed in the `dist` directory.
![Screenshot from 2023-08-31 02-38-22](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/33a5b335-cb62-4cac-8ea1-187150db682c)

![image](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/296bbc62-16ed-41d4-81d6-d5023355ca68)


4. **Uploading to PyPI**: The script will prompt you to enter your PyPI username and password securely. It will then upload the module to PyPI using Twine.

5. **Installing the Module**: After successful upload, you will have the option to install the module using pip for testing purposes.
![Screenshot from 2023-08-31 02-38-55](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/d48027cf-61ba-496e-9b02-8e50db60021c)



## Example

```bash
$ python3 upload_to_pypi.py
# Output will guide you through the process
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to create an issue or submit a pull request.

## License

This utility script is open-source and distributed under the [MIT License](LICENSE).

## Acknowledgments

This script utilizes the following packages and resources:

- [pexpect](https://pexpect.readthedocs.io/) - For automating interactive command-line applications.
- [Twine](https://twine.readthedocs.io/) - For securely uploading Python packages to PyPI.
- [Python](https://www.python.org/) - The Python programming language.

## Disclaimer

This script is provided "as is" without warranty of any kind. Use it at your own risk.

## Support

If you encounter any issues or need assistance, please [create an issue](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_modules) or seek support in the Python community forums.

---

Thank you for using our utility script! If you have any feedback or questions, don't hesitate to contact us. Happy packaging and distributing!
