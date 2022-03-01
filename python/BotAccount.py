
from ConnectionController import ConnectionController
import os
from dotenv import load_dotenv
load_dotenv()

class BotAccount():
    def __init__(self, web3):
        self.connection = web3
        self.account = self.connection.web3.eth.account.create()
        faucet_account = self.connection.web3.eth.account.privateKeyToAccount(os.getenv('FAUCET_PK'))
        nonce = self.connection.web3.eth.getTransactionCount(faucet_account.address)
        self.contracts = []

        #@TODO: move this dict to ConnectionController
        tx = {
            'nonce': nonce,
            'chainId':self.connection.CHAIN_ID,
            'to': self.account.address,
            'value':  self.connection.web3.toWei(0.5, 'ether'),
            'gas': 2000000,
            'gasPrice':  self.connection.web3.toWei('10', 'gwei')
        }
        
        signed_tx = faucet_account.sign_transaction(tx)
        tx_hash = self.connection.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.connection.web3.eth.waitForTransactionReceipt(tx_hash)
        print("\n\nfunding wallet account from faucet:\n\n"+str(tx_receipt))

    def addContract(self, contract):
        self.contracts.append(contract)
    
    def getLatestContract(self):
        return self.contracts[-1]

    
