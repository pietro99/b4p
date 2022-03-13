from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from dotenv import load_dotenv
from ens import ENS

load_dotenv()

class ConnectionController():
    def __init__(self, network = "polygon", mainnet = False):
        infura_id = os.getenv('INFURA_ETH_ID')
        self.network = network

        if self.network == "polygon":
            if mainnet:
                self.provider = Web3.HTTPProvider("https://polygon-rpc.com/")
                self.chain_id = 137
            else:
                self.provider = Web3.HTTPProvider("https://rpc-mumbai.matic.today")
                self.chain_id = 80001
        elif self.network == "ethereum":
            if mainnet:
                self.provider = Web3.HTTPProvider("https://mainnet.infura.io/v3/"+infura_id)
                self.chain_id = 1
            else:
                self.provider = Web3.HTTPProvider("https://rinkeby.infura.io/v3/"+infura_id)
                self.chain_id = 4

        elif self.network == "ganache":
            self.provider = Web3.HTTPProvider('http://127.0.0.1:8545')
            self.chain_id = 1337
        else:
            raise ValueError("network value of "+network+" is not a valid option. choose between polygon (default) and ethereum")

        self.web3 = Web3(self.provider)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.ns = ENS.fromWeb3(self.web3)

class Connect():
    def __init__(self, connection):
        self.connection = connection
        
    @property
    def web3(self):
        return self.connection.web3

    @property
    def chain_id(self):
        return self.connection.chain_id
    
    @property
    def network(self):
        return self.connection.network




        

       
        



    





   