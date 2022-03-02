RELATIVE_CONTRACT_PATH = "../contracts/"
from connection import Connect
import solcx as solcx
import os

#@TODO: change to manage only one contract at the time
class ContractManager(Connect):
    def __init__(self, conn):
        super().__init__(conn)
        self.contracts_names = ["EnergyToken"]
        self.contracts_path = RELATIVE_CONTRACT_PATH
        self.contracts = {}
        self.contracts_addresses = []
        final_path = []
        for contractName in self.contracts_names:
            final_path.append(self.contracts_path + contractName + ".sol")
        
        counter = 0
        for path in final_path:
            with open(path, "r") as f:
                while(True):
                    try:
                        contract_source = f.read()

                        compiled_solc = solcx.compile_source(
                            contract_source,
                            output_values=["abi", "bin"],
                            solc_version=os.getenv('SOLIDITY_V'),
                            base_path=os.path.abspath(RELATIVE_CONTRACT_PATH)
                        )

                        contract_interface = compiled_solc['<stdin>:'+self.contracts_names[counter]]
                        temp_contract = self.web3.eth.contract(abi = contract_interface['abi'], bytecode = contract_interface['bin'])
                        self.contracts[self.contracts_names[counter]] = temp_contract
                        counter += 1
                        break
                    except solcx.exceptions.SolcNotInstalled as e:
                        print("solcx correct version not installed. we are installing it for you")
                        solcx.install_solc(os.getenv('SOLIDITY_V'))    
    
    # This function is used to deploy a contract
    # contract_name: The name (string) of the contract to be deployed
    # wallet: The wallet performing the deployment
    # **kwargs: the arguments that will be passed to the contract's constructor
    # returns: the transaction receipt
    def deploy(self, contract_name,wallet,**kwargs):
        args = kwargs.values()
        try:
            contract = self.contracts[contract_name]
        except KeyError as e:
            raise KeyError(contract_name+" was not as a compiled contract.")
        transaction_dict = {}
        transaction_dict["nonce"] = self.web3.eth.get_transaction_count(wallet.account.address)
        transaction_dict["from"] = wallet.account.address
        transaction_dict["chainId"] = self.chain_id
        contract_function = getattr(contract, "constructor")
        gas = contract_function(*args).estimateGas()
        transaction_dict["gas"] = gas*2 #@NOTE: using gas value will run out of gas so i use gas*2
        transaction_dict["gasPrice"] = self.web3.eth.gas_price
        tx = contract_function(*args).buildTransaction(transaction_dict)
        signed_txn = wallet.account.signTransaction(tx)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt["contractAddress"]
        abi = self.contracts[contract_name].abi
        contract_instance = self.web3.eth.contract(address = contract_address, abi=abi)
        wallet.addContract(contract_instance)
        return tx_receipt

    # This function is used to call a contract's function
    # contract: The contract object containing the function
    # function_name: the name (string) of the function 
    # wallet: The wallet performing the transaction
    # **kwargs: the arguments that will be passed to the contract's function 
    # returns: the transaction receipt
    # @NOTE: if the solidity function returns a value it will not be available here. use call() instead.
    def call(self,contract,function_name, wallet, **kwargs):
        value = kwargs.pop('value') if "value" in kwargs.keys() else 0
        args = kwargs.values()
        transaction_dict = {}
        transaction_dict["from"] = wallet.account.address
        transaction_dict["value"] = value
        contract_function = getattr(contract.functions, function_name)
        gas = contract_function(*args).estimateGas(transaction_dict)
        transaction_dict["gas"] = gas*2 #@NOTE: using gas value will run out of gas so i use gas*2
        transaction_dict["nonce"] = self.web3.eth.get_transaction_count(wallet.account.address)
        transaction_dict["chainId"] = self.chain_id
        transaction_dict["gasPrice"] = self.web3.eth.gas_price
        tx = contract_function(*args).buildTransaction(transaction_dict)
        signed_txn = wallet.account.signTransaction(tx)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    # This function is used to read data from a contract
    # contract: The contract object containing the function
    # function_name: the name (string) of the function 
    # wallet: The wallet performing the transaction
    # **kwargs: the arguments that will be passed to the contract's function
    # returns: the value returned by the contract's function
    # @NOTE: only use this for solidity functions that are "pure" or "view"
    def read(self,contract,function_name,wallet, **kwargs):
        args = kwargs.values()
        transaction_dict = {}
        transaction_dict["nonce"] = self.web3.eth.get_transaction_count(wallet.account.address)
        transaction_dict["from"] = wallet.account.address
        transaction_dict["chainId"] = self.chain_id
        transaction_dict["gasPrice"] = self.web3.eth.gas_price

        contract_function = getattr(contract.functions, function_name)
        gas = contract_function(*args).estimateGas()
        transaction_dict["gas"] = gas*2 #@NOTE: using gas value will run out of gas so i use gas*2
        tx = contract_function(*args).call()
        return tx
 





