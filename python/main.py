from connection import ConnectionController
from contracts import ContractManager
from wallet import TestWallet
from ipfs import IpfsManager


print()

ipfs = IpfsManager()

#establish connection to a network node
conn = ConnectionController(network = "polygon")
if conn.web3.isConnected():
    print("\nsuccessfully connected using "+ str(conn.provider)+"\n")

print("ens: "+str(conn.ns.address("eth-usd.data.eth")))
cm = ContractManager(conn)

#create a bot with a wallet
energyProvider = TestWallet(conn)
energyBuyer = TestWallet(conn)

otherBuyer = TestWallet(conn)


tx = cm.deploy("EnergyToken", energyProvider, metadata_hash = "hash")
ET_address = tx["contractAddress"]

tx = cm.deploy("ERC20", energyProvider, name="examplecoin", symbol="EC")
coin_address = tx["contractAddress"]

#mint a new batch of tokens
tx = cm.call(energyProvider.getContract(ET_address), "addEnergyBatch", energyProvider, energy=100, amount=1000)

tx = cm.call(energyProvider.getContract(ET_address), "setForSale",energyProvider, id=1, amount=10, price=1000)

#reading token id and transaction price for following function
token_id = cm.read(energyProvider.getContract(ET_address), "energyToToken", energy=100)
price = cm.read(energyProvider.getContract(ET_address), "getPrice", id=token_id, amount=100)

#buy token
tx = cm.call(energyProvider.getContract(ET_address), "safeBuy", energyBuyer, id=token_id, amount=100, value=price)


#buy token
tx = cm.call(energyProvider.getContract(ET_address), "setForSale", energyBuyer, id=token_id, amount=50, price=2000)

#reading token id and transaction price for following function
token_id = cm.read(energyProvider.getContract(ET_address), "energyToToken", energy=100)
price = cm.read(energyProvider.getContract(ET_address), "getPrice", id=token_id, amount=25)
tx = cm.call(energyProvider.getContract(ET_address), "safeBuy", otherBuyer, id=token_id, amount=25, price=price)


contractbalance = cm.read(energyProvider.getContract(ET_address), "totalBalance")

print(f"\nbuyer's balance: {energyBuyer.balance()}")
print(f"provider's balance: {energyProvider.balance()}")
print(f"contract's balance: "+str(conn.web3.fromWei(contractbalance, "ether")))

tx = cm.call(energyProvider.getContract(ET_address), "withdrawAllFunds", energyProvider)

contractbalance = cm.read(energyProvider.getContract(ET_address), "totalBalance")

print("\nafter withdrawl:\n")
print(f"buyer's balance: {energyBuyer.balance()}")
print(f"provider's balance: {energyProvider.balance()}")
print(f"contract's balance: "+str(conn.web3.fromWei(contractbalance, "ether")))
