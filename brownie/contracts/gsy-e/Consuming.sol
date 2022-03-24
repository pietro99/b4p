// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC20/ERC20.sol)
pragma solidity ^0.8.12;

import "./Structs.sol";
import "./Node.sol";
import "./Structs.sol";


contract Consuming {

uint capacity;
uint production_rate;
uint current_offer;
Node connected_node;

constructor(uint _capacity, uint _production_rate, uint _current_offer, address node){
    capacity = _capacity;
    production_rate = _production_rate;
    current_offer = _current_offer;
    connected_node = Node(node);
}

function timeTick() external view returns(Node,SharedStructs.OfferOrBid memory){
    SharedStructs.OfferOrBid memory offer = SharedStructs.OfferOrBid(true, block.timestamp, current_offer, production_rate, address(this));
    return (connected_node, offer);
}




}