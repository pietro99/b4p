
from connection import ConnectionController, Connect
import os
from dotenv import load_dotenv
load_dotenv()




# @NOTE: this will probably be modified to a system where the wallet object 
# only contains the public key and signs transactions per request. it 
# should also contain encryption methods. TBD when we understand how to 
# deal with keys 
class Wallet(Connect):
    def __init__(self, conn, private_key=""):
        super().__init__(conn)
        self.account = False
        if private_key != "":
             self.account = self.web3.eth.account.privateKeyToAccount(private_key)
        self.contracts = []

    def createAccount(self):
        self.account = self.web3.eth.account.create() 

    def fundAccount(self):
        self.faucet.sendEther(self.account, FUND_AMOUNT)

    def sendEther(self, wallet, amount, denomination = "ether"):
        nonce = self.web3.eth.getTransactionCount(self.account.address)
        tx = {
            'nonce': nonce,
            'chainId':self.chain_id,
            'to': wallet.account.address,
            'value':  self.web3.toWei(amount, denomination),
            'gas': 2000000,
            'gasPrice':  self.web3.toWei('50', 'gwei')
        }
        signed_tx = self.account.sign_transaction(tx)

        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return self.web3.eth.waitForTransactionReceipt(tx_hash)


    def addContract(self, contract):
        self.contracts.append(contract)
    
    def getLatestContract(self):
        return self.contracts[-1]


FUND_AMOUNT = 0.5 #amount sent when funding 

class TestWallet(Wallet):
    def __init__(self, conn, fund=True):
        super().__init__(conn)
        self.createAccount()
        if self.network == "ganache":
            self.faucet = Wallet(conn, os.getenv('GANACHE_PK'))
        else:
            self.faucet = Wallet(conn, os.getenv('FAUCET_PK'))
        if fund:
            tx_receipt = self.fundAccount()
            print("\nfunding new wallet account from faucet:\n"+str(tx_receipt["transactionHash"].hex()))


    def fundAccount(self):
        return self.faucet.sendEther(self, FUND_AMOUNT)
