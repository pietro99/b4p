from connection import ConnectionController
from contracts import ContractManager
from wallet import TestWallet
from ipfs import IpfsManager

ipfs = IpfsManager()

#establish connection to a network node
conn = ConnectionController(network = "ganache")
if conn.web3.isConnected():
    print("\nsuccessfully connected using "+ str(conn.provider)+"\n")

cm = ContractManager(conn)


#create a bot with a wallet
energyProvider = TestWallet(conn)
energyBuyer = TestWallet(conn)

#example of token metadata
token_metadata = {
    "location" : {"latitude":51.427985, "longitude":5.683654},
    "type" : "wind turbine"
}

#adding the metadata to ipfs
hash = ipfs.add(token_metadata)["Hash"]
print(f"\nmetadata posted to ipfs --> {hash}")

#deploy Token Contract with ipfs hash
tx = cm.deploy("EnergyToken", energyProvider, metadata_hash = hash)
print("\ndeployment of Energy token:\ntransaction hash --> "+str(tx["transactionHash"].hex()))

#mint a new batch of tokens
tx = cm.call(energyProvider.getLatestContract(), "addEnergyBatch", energyProvider, energy=100, amount=1000, price = 10000000000)
print(f"\nminting energy tokens:\ntransaction hash --> "+str(tx["transactionHash"].hex()))

#retriving metadata hash
hash = cm.read(energyProvider.getLatestContract(), "uri", energyBuyer, _id = 1)
print(f"\nmetadata retrieved from ipfs --> {hash}")

#reading metadata from ipfs
metadata = ipfs.cat(hash)
print(f"\nmetadata of token:\n{metadata}")

#reading token id and transaction price for following function
token_id = cm.read(energyProvider.getLatestContract(), "energyToToken", energyBuyer, energy=100)
price = cm.read(energyProvider.getLatestContract(), "getPrice",energyBuyer, id=token_id, amount=1000)

#buy token
tx = cm.call(energyProvider.getLatestContract(), "safeBuy", energyProvider, id=token_id, amount=1000, value=price)
print(f"\nbuying tokens\ntransaction hash: "+str(tx["transactionHash"].hex()))
