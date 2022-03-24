// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC20/ERC20.sol)
pragma solidity ^0.8.12;

import "./Structs.sol";
import "./Node.sol";
import "./Producing.sol";
import "./Consuming.sol";

contract MarketOp {
    Node[] nodes;
    Producing[] producing;
    Consuming[] consuming;

    mapping(Node => SharedStructs.OfferOrBid[]) offers;

    function update() external  {
        for(uint i=0; i<producing.length; i++){
            Producing curr_producing = producing[i];
            (Node next_node, SharedStructs.OfferOrBid memory offer ) = curr_producing.timeTick();
            nodes.push(next_node);
            offers[next_node].push(offer);
        }
        for(uint i=0; i<consuming.length; i++){
            Consuming curr_consuming = consuming[i];
            (Node next_node, SharedStructs.OfferOrBid memory bid ) = curr_consuming.timeTick();
            nodes.push(next_node);//@BUG: double addresses in nodes array
            offers[next_node].push(bid);
        }

        for(uint i=0; i<nodes.length; i++){
            Node node = nodes[i];
            node.checkMatch(offers[node]);
        }
        
    }
}