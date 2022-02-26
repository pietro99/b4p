from ConnectionController import ConnectionController, ContractManager
from BotAccount import BotAccount

#establish connection to a network node
conn = ConnectionController(network = "polygon")
if conn.web3.isConnected():
    print("\nsuccessfully connected using "+ str(conn.provider)+"\n")

cm = ContractManager(conn)

#create a bot with a wallet
bot1 = BotAccount(conn)

#deploy Token Contract
tx1 = cm.deploy("EnergyToken", "constructor", bot1, "https://metadata.com/")
print("\n\ndeployment transaction:\n"+str(tx1))

#read address of contract owner
tx2 = cm.read(bot1.getLatestContract(), "energyProvider", bot1)
print("\n\nenergy provider address:\n\n"+str(tx2))

#mint a new batch of 1000 tokens representing 100kw each
tx3 = cm.call(bot1.getLatestContract(), "addEnergyBatch", bot1, energy=100, amount=1000)
print("\n\ntoken mint transaction:\n\n"+str(tx3))

