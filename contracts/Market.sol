// SPDX-License-Identifier: MIT
pragma solidity ^0.8.12;

import "./openzeppelin/contracts/utils/Address.sol";
import "./EnergyToken.sol";

contract EnergyMarket {
    using Address for address;
    address private admin;
    mapping(address => EnergyToken) public tokens;
    
    constructor(){
        admin = msg.sender;
    }

    function receiveToken(address _tokeAddress) public{
        tokens[_tokeAddress] = EnergyToken(_tokeAddress);
    }

    function coinBalance(address _tokeAddress, uint _id) public view returns(uint){
        return tokens[_tokeAddress].balanceOf(address(this), _id);
    }



}