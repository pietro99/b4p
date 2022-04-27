# b4p contracts
:warning: **work in progress** :warning:	


this repository contains the environment to develop and test the smart contracts that model a spot energy market. This repository

## setup

### api keys
this project will require an alchemy api key as well as a etherscan api key. requesting both api keys is free for a limited use.

to create an alchemy api key you can create an account [here](https://www.alchemy.com/) and create a new app on the ethereum chain and the mainnet network (brownie will use the mainnet node provided by alchemy to fork the mainnet network in a local development network).

you can request an api from etherescan by creating an account [here](https://etherscan.io/register) and requesting the key from the account settings.
the etherscan api key will be used by brownie to pull existing contract such as the [EURS contract](https://etherscan.io/address/0xdB25f211AB05b1c97D595516F45794528a807ad8) 

once both the keys are obtained they should be put in a .env configuration file. an example of it it's found in the [example.env](example.env).
please note that the names of the environment variables need to be exactly as in the example.env file so that brownie will know how to use them.

### environment setup

it is adivisable to first create a python environment to avoid dependencies clashes by runnig

```
python -m venv python_env 
```
then to activate it run
```
python_env\Scripts\activate
```

next install the python requirements by runnig

```
pip install -r requirements.txt
```


## use

### scripts

the main example script can be run using

```
brownie run market.py
```

this will crete all of the transactions to set up an energy market and run an example inspired by the grid singlularity example [here](https://gridsingularity.github.io/gsy-e/constant-fees/) in **Figure 3.16**


## testing

to run all of the test use

```
brownie run test
```



