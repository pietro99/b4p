from brownie import accounts, network, config, Market
from scripts.helper import get_account, get_contract, generate_accounts, get_latest_accounts
from web3 import Web3
from time import time

def main():
    market = Market.deploy({"from":accounts[0]})
    SCtime = market.receiveOffer(10,10, {"from":accounts[0]})
    SCtime.wait(1)
    offers = market.offers(0)
    print(offers)
