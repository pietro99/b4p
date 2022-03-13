from brownie import accounts, network, config, EnergyToken, MockV3Aggregator, Contract, interface
from scripts.helper import get_account, get_contract, generate_accounts, get_latest_accounts
from web3 import Web3


GAS_PRICE = "30 gwei"
def deploy(provider):
    EnergyToken.deploy("hash",{"from":provider, "gas_price":GAS_PRICE}, publish_source=config["networks"][network.show_active()].get("verify"))
    
def addEnergyBatch(provider,amount):
    energyToken = EnergyToken[-1]
    tx = energyToken.addEnergyBatch(100, amount,{"from":provider.address, "gas_price":GAS_PRICE})
    tx.wait(1)

def setForSale(seller, amount, price):
    energyToken = EnergyToken[-1]
    tx = energyToken.setForSale(1, amount, price,{"from":seller.address, "gas_price":GAS_PRICE})
    tx.wait(1)


def safeBuy(buyer,provider, amount):
    energyToken = EnergyToken[-1]
    price = energyToken.getPrice(1, amount, provider.address,{"from":buyer.address})
    tx = energyToken.safeBuy(1, amount, provider.address, {"from": buyer.address, "value":price, "gas_price":GAS_PRICE})
    tx.wait(1)

def print_status():
    provider, buyer, secondbuyer = get_latest_accounts(3)
    print(f"provider: {EnergyToken[-1].balanceOf(provider, 1)} EnergyTokens | {Web3.fromWei(provider.balance(), 'ether')} ether")
    print(f"first buyer: {EnergyToken[-1].balanceOf(buyer, 1)} EnergyTokens | {Web3.fromWei(buyer.balance(), 'ether')} ether")
    print(f"second buyer: {EnergyToken[-1].balanceOf(secondbuyer, 1)} EnergyTokens | {Web3.fromWei(secondbuyer.balance(), 'ether' )} ether")


def sendToken():
    link = interface.IERC20(config["networks"][network.show_active()].get("link"))
    faucet = accounts.add(config["wallets"]["faucet"])
    link.approve(EnergyToken[-1], Web3.toWei(1, "ether"), {"from":faucet,"gas_price":GAS_PRICE})
    #link.transfer("0x1A5022ED8d0A1597217928064D97B3F341CEC0c4", link.balanceOf(faucet), {"from":faucet})
    EnergyToken[-1].buyWithToken(link, Web3.toWei(1, "ether"),{"from":faucet,"gas_price":GAS_PRICE, "allow_revert":True})




def main():
    if network.show_active() != "development":
        generate_accounts(3)
    provider, buyer, secondbuyer = get_latest_accounts(3)
    deploy(provider)
    addEnergyBatch(provider, 1000)
    setForSale(provider, 50, Web3.toWei(0.0001, "ether"))   
    print_status()
    safeBuy(buyer, provider, 50)
    print_status()  
    setForSale(buyer, 30 , Web3.toWei(0.0002, "ether"))
    safeBuy(secondbuyer,buyer, 10)
    print_status()
    sendToken()
    


