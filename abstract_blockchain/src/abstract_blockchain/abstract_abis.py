def list_contract_functions(abi):
    functions = []
    for item in abi:
        if item['type'] == 'function':
            function_details = {
                "name": item['name'],
                "inputs": [(i['name'], i['type']) for i in item['inputs']],
                "outputs": [(o['name'], o['type']) for o in item['outputs']]
            }
            functions.append(function_details)
    return functions

def main():
    address = input("Enter Ethereum contract address: ")
    abi = get_contract_abi(address)
    functions = list_contract_functions(abi)
