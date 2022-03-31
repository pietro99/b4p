from brownie import accounts,Contract, network, config, Market,config, ERC20Test
from scripts.helper import get_account, get_contract, generate_accounts, get_latest_accounts
from web3 import Web3
from time import time
import json 


def print_balances(eurs):
    market = Market[-1]
    enrgyToken = ERC20Test[-1]
    print("\neurs:")
    print(f'EURS bidder {eurs.balanceOf(accounts[0])}')
    print(f'EURS offerer {eurs.balanceOf(accounts[1])}')
    print(f'EURS market {eurs.balanceOf(market)}')
    print("\nenergy token:")
    print(f'EnergyTokens bidder {enrgyToken.balanceOf(accounts[0])}')
    print(f'EnergyTokens offerer {enrgyToken.balanceOf(accounts[1])}')
    print(f'EnergyTokens market {enrgyToken.balanceOf(market)}\n')



def getEURS(account):
    eurs_address = config["networks"][network.show_active()].get("eurs")
    eurs = Contract.from_explorer(eurs_address)
    tx = eurs.transfer(account, 1000, {"from":eurs_address})
    tx.wait(1)
    return eurs

def main():
    print("\n############### SETUP TRANSACTIONS ###############\n")
    eurs = getEURS(accounts[0])

    #deployments
    energyToken = ERC20Test.deploy({"from":accounts[0]})
    market = Market.deploy(eurs,energyToken, {"from":accounts[0]})

    market = Market[-1]
    enrgyToken = ERC20Test[-1]

    #approve Market to use tokens
    eurs.approve(market, 2**200, {"from":accounts[0]})
    enrgyToken.approve(market, 2*200, {"from":accounts[1]})

    print("\n############### MARKET TRANSACTIONS ###############\n")

    print_balances(eurs)
    tx = market.receiveOffer(3, 1000, {"from": accounts[1]})
    tx.wait(1)
    #print(tx.events)
    print_balances(eurs)

    
    tx = market.receiveBid(5, 10, {"from": accounts[0]})
    tx.wait(1)
    #print(tx.events)
    print_balances(eurs)

   
