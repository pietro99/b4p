// SPDX-License-Identifier: MIT

pragma solidity ^0.8.12;

import "./EnergyToken.sol";
import "./Market.sol";
import "./Node.sol";
abstract contract Asset is Node {
    EnergyToken token;
    address owner;

    constructor( 
    address ownerAddress, 
    address _marketAddress) 
    Node(_marketAddress){
        owner = ownerAddress;
        token = EnergyToken(market.energyToken());
    }
}