# Blockchain 4 Prosumer project
## Getting started

##### cloning the repository
The code implements the ERC1155 and other utility contracts from the [openzeppeling contract library](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/abdb20a6bdb1700d58ea9e01b7471dafdef52a68) located in the [contracts](/contracts) folder.
In order to clone the repo together with the submodules run 
```bat
git clone --recurse-submodules https://github.com/pietro99/b4p.git
```
If you have already cloned the repository you can pull the submodule by:
```bat
git submodule update --init --recursive
```
##### setting environments variables
create .env file inside the [python](/python) folder and copy the [.env.example](/python/.env.example) file to it.
the code uses an [infura](https://infura.io/) node to connect to the mumbai testnetwork and a private key from a wallet as a faucet to fund the test wallets.
you will need to provide your own key and id inside the .env file, the placeholder values are fake. **(do not use a private key from an active mainnet wallet)**


