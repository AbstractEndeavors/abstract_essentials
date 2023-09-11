---

# Abstract Blockchain Package

The **Abstract Blockchain** package provides a collection of modules designed to simplify interaction with blockchain networks, smart contracts, and related components. It offers tools for managing RPC parameters, working with smart contract ABIs, and facilitating user-friendly interactions through graphical user interfaces (GUIs).

## Modules

### `abstract_abis.py`

This module provides the `ABIBridge` class, which serves as an interface to Ethereum smart contract ABIs. It allows you to interact with contract functions, retrieve read-only functions, get required input details, and call contract functions using a convenient interface. Additionally, it provides methods for fetching and categorizing RPC parameters for blockchain interaction.

### `abstract_apis.py`

This module offers the `RPCData` class that handles the management of RPC parameters for blockchain networks. It enables users to filter and select RPC parameters through a graphical user interface (GUI). The class also categorizes and organizes RPC parameters for ease of use in blockchain interactions.

### `abstract_rpcs.py`

This module provides utilities for working with blockchain RPC parameters. It includes functions to filter and categorize RPC parameters, organize them into sub-lists based on keys, and create a GUI for users to choose specific RPC parameters for blockchain interactions.

### `abstract_utilities`

This submodule contains utility functions used across the package for tasks such as working with JSON data, managing lists, and GUI components.

### `abstract_gui`

This submodule provides utilities for creating graphical user interfaces (GUIs) that enhance user interaction with blockchain-related features. It offers functions for creating windows, buttons, menus, and more, streamlining the process of building user-friendly interfaces.
![Screenshot from 2023-09-11 09-46-43](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/ae2017c7-542d-4353-be3d-9c71945bb3ab)
![Screenshot from 2023-09-11 09-46-37](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/a102e01c-cee0-4c55-903f-bf490be74ae4)
![Screenshot from 2023-09-04 05-07-39](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/70df9d24-62d0-4172-8870-b0df272748ce)
![Screenshot from 2023-09-04 05-07-06](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/002cd61a-427b-4642-8d4d-14594cf22cd1)

## Example Usage

```python
from abstract_abis import ABIBridge
from abstract_apis import Choose_RPC_Parameters_GUI, RPCData

# Example usage of ABIBridge
abi_manager = ABIBridge(contract_address='0x3dCCeAE634f371E779c894A1cEa43a09C23af8d5', rpc=default_rpc())
read_only_functions = abi_manager.get_read_only_functions()
for each in read_only_functions:
    inputs = abi_manager.get_required_inputs(each)
    if len(inputs) == 0:
        result = abi_manager.call_function(each)
        print(each, result)
    else:
        print(each, inputs)

# Example usage of RPCData and GUI
rpc_data = Choose_RPC_Parameters_GUI()
rpc_manager = RPCData(rpc_data)
w3 = rpc_manager.w3

# Your blockchain interactions using w3...
```

## Installation

The `abstract_blockchain` package can be installed using pip:

```bash
pip install abstract_blockchain
```

## License

This package is released under the [MIT License](LICENSE).

---

