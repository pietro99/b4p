// SPDX-License-Identifier: MIT

pragma solidity ^0.8.12;
import "./Asset.sol";
contract ConsumingAsset is Asset{
  
    constructor( address _marketAddress) Asset( msg.sender, _marketAddress) {}

    function forward(OfferOrBid memory offer) override internal {
        market.receiveBid(offer);
    }
    function createBid(uint price, uint amount) public {
        OfferOrBid memory offer = OfferOrBid(block.timestamp, price, amount, address(this));
        forward(offer);
    }
   
}