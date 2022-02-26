from web3 import Web3
import os
from dotenv import load_dotenv
import solcx as solcx
load_dotenv()
RELATIVE_CONTRACT_PATH = "../contracts/"

class ConnectionController():
    def __init__(self, network = "polygon", mainnet = False):
        infura_id = os.getenv('INFURA_ID')
        self.network = network
        if self.network == "polygon":
            if mainnet:
                self.provider = Web3.HTTPProvider("https://polygon-rpc.com/")
                self.CHAIN_ID = 137
            else:
                self.provider = Web3.HTTPProvider("https://rpc-mumbai.matic.today")
                self.CHAIN_ID = 80001
        elif self.network == "ethereum":
            if mainnet:
                self.provider = Web3.HTTPProvider("https://mainnet.infura.io/v3/"+infura_id)
                self.CHAIN_ID = 1
            else:
                self.provider = Web3.HTTPProvider("https://rinkeby.infura.io/v3/"+infura_id)
                self.CHAIN_ID = 4
        else:
            raise ValueError("network value of "+network+" is not a valid option. choose between polygon (default) and ethereum")


        self.web3 = Web3(self.provider)
        self.transaction_dict = {
            "chainId": self.CHAIN_ID,
        }

class ContractManager():
    def __init__(self, web3):
        self.connection = web3
        self.contracts_names = ["EnergyToken", "EnergyProviders"]
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
                        compiled_solc = solcx.compile_source(contract_source,output_values=["abi", "bin"],solc_version=os.getenv('SOLIDITY_V'), base_path=os.path.abspath(RELATIVE_CONTRACT_PATH))
                        contract_interface = compiled_solc['<stdin>:'+self.contracts_names[counter]]
                        temp_contract = self.connection.web3.eth.contract(abi = contract_interface['abi'], bytecode = contract_interface['bin'])
                        self.contracts[self.contracts_names[counter]] = temp_contract
                        counter += 1
                        break
                    except solcx.exceptions.SolcNotInstalled as e:
                        print("solcx correct version not installed. we are installing it for you")
                        solcx.install_solc(os.getenv('SOLIDITY_V'))    

    def deploy(self, contract_name, function_name,account,*args):
        try:
            contract = self.contracts[contract_name]
        except KeyError as e:
            raise KeyError(contract_name+" was not as a compiled contract.")
        transaction_dict = self.connection.transaction_dict
        transaction_dict["nonce"] = self.connection.web3.eth.get_transaction_count(account.account.address)
        transaction_dict["from"] = account.account.address
        if function_name == "constructor":
            contract_function = getattr(contract, function_name)
        else:
            contract_function = getattr(contract.functions, function_name)
        gas = contract_function(*args).estimateGas()
        transaction_dict["gas"] = gas*2
        tx = contract_function(*args).buildTransaction(transaction_dict)
        signed_txn = account.account.signTransaction(tx)
        tx_hash = self.connection.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.connection.web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt["contractAddress"]
        abi = self.contracts[contract_name].abi
        contract_instance = self.connection.web3.eth.contract(address = contract_address, abi=abi)
        account.addContract(contract_instance)
        return tx_receipt

    def call(self,contract,function_name,account, **kwargs):
        args = kwargs.values()
        transaction_dict = self.connection.transaction_dict
        transaction_dict["nonce"] = self.connection.web3.eth.get_transaction_count(account.account.address)
        transaction_dict["from"] = account.account.address
        if function_name == "constructor":
            contract_function = getattr(contract, function_name)
        else:
            contract_function = getattr(contract.functions, function_name)
        gas = contract_function(*args).estimateGas({"from":account.account.address})
        transaction_dict["gas"] = gas*2
        tx = contract_function(*args).buildTransaction(transaction_dict)
        signed_txn = account.account.signTransaction(tx)
        tx_hash = self.connection.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.connection.web3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt
    
    def read(self,contract,function_name,account, *args):
        transaction_dict = self.connection.transaction_dict
        transaction_dict["nonce"] = self.connection.web3.eth.get_transaction_count(account.account.address)
        transaction_dict["from"] = account.account.address
        if function_name == "constructor":
            contract_function = getattr(contract, function_name)
        else:
            contract_function = getattr(contract.functions, function_name)
        gas = contract_function(*args).estimateGas()
        transaction_dict["gas"] = gas*2
        tx = contract_function(*args).call()
        return tx
 








        

       
        



    





   