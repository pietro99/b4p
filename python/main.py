from ConnectionController import ConnectionController, ContractManager
from BotAccount import BotAccount

#establish connection to a network node
conn = ConnectionController(network = "polygon")
if conn.web3.isConnected():
    print("\nsuccessfully connected using "+ str(conn.provider)+"\n")

cm = ContractManager(conn)

#create a bot with a wallet
energyProvider = BotAccount(conn)
energyBuyer = BotAccount(conn)


#deploy Token Contract
tx1 = cm.deploy("EnergyToken", energyProvider, metadata = "https://metadata.com/")
print("\n\ndeployment transaction:\n"+str(tx1))

#read address of contract owner
tx2 = cm.read(energyProvider.getLatestContract(), "owner", energyBuyer)
print("\n\nenergy provider address:\n\n"+str(tx2))

#mint a new batch of 1000 tokens representing 100kw each
tx3 = cm.call(energyProvider.getLatestContract(), "addEnergyBatch", energyProvider, energy=100, amount=1000, price = 10000000000)
print("\n\ntoken mint transaction:\n\n"+str(tx3))

#mint a new batch of 1000 tokens representing 100kw each
token_id = cm.read(energyProvider.getLatestContract(), "energyToToken", energyBuyer, energy=100)
print("\n\ntoken id:\n\n"+str(token_id))

#mint a new batch of 1000 tokens representing 100kw each
price = cm.read(energyProvider.getLatestContract(), "getPrice",energyBuyer, id=token_id, amount=1000)
print("\n\nprice:\n\n"+str(price))


#mint a new batch of 1000 tokens representing 100kw each
tx4 = cm.call(energyProvider.getLatestContract(), "safeBuy", energyProvider, id=token_id, amount=1000, value=price)
print("\n\nbuy transaction: \n\n"+str(tx4))
