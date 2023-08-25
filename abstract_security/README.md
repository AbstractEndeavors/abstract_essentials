```markdown
# Abstract Security

**Abstract Security** is a Python module designed to streamline the management and access of environment variables stored in `.env` files. Its key feature is its ability to search multiple directories for these files, ensuring you always fetch the right environment variables with minimal hassle.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [License](#license)
- [Contact](#contact)

## Features

- **Auto-search**: Automatically looks for `.env` files in a specified directory, the directory from which the function is called, the home directory, and lastly, within a folder named `envy_all`.
- **Flexibility**: Offers an option to specify the path where the `.env` file resides.
- **Safety**: Implements safe loading of `.env` files to avoid any unforeseen errors.

## Installation

```bash
pip install abstract_security
```

## Usage

### Basic Usage

```python
from abstract_security import get_env_value

# Default usage: Retrieve the value of the 'MY_PASSWORD' environment variable from the .env file
password = get_env_value()
```

### Advanced Usage

If you need to specify the `.env` file name or start the search from a different path:

```python
# Specify the path, file name, and key to fetch a value from a specific .env file
value = get_env_value(path='/path/to/directory', file_name='custom.env', key='CUSTOM_KEY')
```

If your `.env` files are located in the `envy_all` directory within your home directory, it's recommended to place all `.env` files there for seamless integration with this module.

## Functions

### `find_and_read_env_file`

Searches for an environment file and reads a specific key from it.

### `search_for_env_key`

Looks for a specific key within a `.env` file and returns its value.

### `check_env_file`

Verifies the existence of the `.env` file within a specified path.

### `safe_env_load`

Ensures the safe loading of a `.env` file, if it exists, at a specified path.

### `get_env_value`

Fetches the value of a specified environment variable. This is the primary function you'd use in most scenarios.

For an in-depth understanding and other functionalities, please refer to the function docstrings within the code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for full details.

## Contact

**Author**: putkoff  
**Email**: partners@abstractendeavors.com  
**Project Link**: [https://github.com/AbstractEndeavors/abstract_essentials/abstract_security](https://github.com/AbstractEndeavors/abstract_essentials/abstract_security)
```

This expanded README provides potential users with a clearer understanding of the features and functionalities of the `abstract_security` module. Adjustments and further additions can be made as needed.
