// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC20/ERC20.sol)
pragma solidity ^0.8.12;
library SharedStructs {
    struct OfferOrBid {
        bool is_bid;
        uint created_at;
        uint price;
        uint amount;
        address producer_address;
    }    
}