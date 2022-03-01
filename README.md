# Blockchain 4 Prosumer project
## Getting started

##### cloning the repository
The code implements the ERC1155 and other utility contracts from the [openzeppeling contract library](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/abdb20a6bdb1700d58ea9e01b7471dafdef52a68) which is included as a submodule located in the [contracts](/contracts) folder.
In order to clone this repository together with the submodule run:
```bat
git clone --recurse-submodules https://github.com/pietro99/b4p.git
```
If you have already cloned the repository you can pull the submodule by:
```bat
git submodule update --init --recursive
```
##### setting environments variables
create a .env file inside the [python](/python) folder and copy the [.env.example](/python/.env.example) file content to it.
the code uses an [infura](https://infura.io/) node to connect to the mumbai testnetwork and a private key from a wallet as an app faucet to fund the test wallets.
you will need to provide your own private key and infura id inside the .env file. **(do not use a private key from an active mainnet wallet)**
the app faucet needs to have at least 0.5 MATIC to be able to fund new accounts. you can fund your mumbai faucet wallet [here](https://faucet.polygon.technology/) or you can use the mumbai faucet programmatically by using the [faucet script](#faucet script)

##### installing python requirements
the python requirements can be installed by running:
```bat
pip install -r ./python/requirements.txt
```
it is advisable to create a fresh python environment before installing the requirements to avoid clonficts.

##### running the code
finally the code can be tested by running:
```bat
cd python
python main.py
```

##### faucet script

the [faucet script](/python/faucet_script.py) can be called by running `python faucet_script.py` and it will request 0.5 MATIC of funds from the official mumbai faucet to your app faucet (specified in the .env file). the request are made approximately once every 60 seconds. keep in mind that many times the request is not successfull and that the mumbai faucet will not accept requests from wallets with a balance greater than 10 MATIC which should be enough for testing the smart contracts.



