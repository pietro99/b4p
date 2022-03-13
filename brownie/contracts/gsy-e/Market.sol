// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC20/ERC20.sol)
pragma solidity ^0.8.12;

import "./Structs.sol";
import "./Node.sol";
import "./Producing.sol";
import "./Consuming.sol";

contract Market {
    Node[] nodes;
    Producing[] producing;
    Consuming[] consuming;

    mapping(Node => SharedStructs.OfferOrBid[]) offers;

    function update() external  {
        for(uint i=0; i<producing.length; i++){
            Producing curr_producing = producing[i];
            (Node next_node, SharedStructs.OfferOrBid memory offer ) = curr_producing.timeTick();
            node.
        }
        
    }
}