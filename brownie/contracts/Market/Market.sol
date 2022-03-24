// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC20/ERC20.sol)
pragma solidity ^0.8.12;
import "./ERC20Test.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

/*
    Missing: 
- timestamp for when the energy is required
- network structure of market + propagation bids/offers
- reliable transfer of stablecoin

    Questions:
- purpose of energy token??
- minting and burning of ET
- who holds energy token?

*/
contract Market is ERC20Test{
    using Counters for Counters.Counter;

    //event that is raised when an offer and a bid match
    event Match(uint price, uint amount, uint timesatmp, address bidAddress, address offerAddress);


    struct OfferOrBid {
        uint created_at;
        uint price;
        uint amount;
        address _address;
    }

    IERC20 stableCoin;
    //AggregatorV3Interface priceFeed;

    //offers in the market
    mapping(uint => OfferOrBid) public offers; 
    //bids in the market 
    mapping(uint => OfferOrBid) public bids;  

    //stable coin balances
    mapping(address => uint) public usdBalance;

    //track lenght of offers and bids
    Counters.Counter offersLength;
    Counters.Counter bidsLength;
    
    //deploy with a stablecoint (e.g Thether USD)
    //the price in bid/offers will refer to this stablecoin
    constructor(address stableCoinAddress){
        stableCoin = IERC20(stableCoinAddress);
    }

    // energy providers will call this function sepcifying the price and a 
    // max amount of energy availabe to sell
    function receiveOffer(uint price, uint maxamount) public{
        OfferOrBid memory offer = OfferOrBid(block.timestamp, price, maxamount, msg.sender);
        _mint(offer._address, offer.amount);
        bool offerMatched = _checkMatchOffer(offer);
        if(!offerMatched || offer.amount != 0){
            offers[offersLength.current()] = offer;
            offersLength.increment();
        }   
    }

    //energy consumer will call this function specigying the price and 
    //the amount they need.
    //the stable coins will be transferred to the smart contract untill an offer matches 
    //then they will be transferred to the provider.
    function receiveBid(uint price, uint amount) public {
        OfferOrBid memory bid = OfferOrBid(block.timestamp, price, amount, msg.sender);
        stableCoin.transferFrom(msg.sender, address(this), price*amount);
        usdBalance[msg.sender] += price*amount;
        bool bidMatched = _checkMatchBid(bid);
        if(!bidMatched){
            bids[bidsLength.current()] = bid;
            bidsLength.increment();
        }
    }

    //check when a new offer enters the market if it has a match
    //if a match is found remove the bid
    function _checkMatchOffer(OfferOrBid memory offer) internal returns(bool) {
        for(uint i=0; i<bidsLength.current(); i++){
            OfferOrBid memory bid = bids[i];
            if(_match(bid, offer)){
                _removeBid(i);
                return true;
            }
        } 
        return false;
    }

    //chekc when a new bid enters the market if it has a match
    function _checkMatchBid(OfferOrBid memory bid) internal returns(bool) {
        for(uint i=0; i<offersLength.current(); i++){
            OfferOrBid memory offer = offers[i];
            if(_match(bid, offer)){
                if(offer.amount == 0)
                    _removeOffer(i);
                return true;
            }

        } 
        return false;
    }


    function _match(OfferOrBid memory bid, OfferOrBid memory offer) internal returns(bool) {
        if(bid.price >= offer.price && bid.amount<= offer.amount){
            emit Match(bid.price, bid.amount, block.timestamp, bid._address, offer._address);
            approve(bid._address, bid.amount);
            transferFrom(offer._address, bid._address, bid.amount);
            stableCoin.transferFrom(address(this), offer._address, bid.amount*bid.price);
            offer.amount = offer.amount - bid.amount;
            return true;
        }
        return false;
    }


    function _removeBid(uint index)  public {
        require(index < bidsLength.current(), "wrong lenght");

        for (uint i = index; i<bidsLength.current()-1; i++){
            bids[i] = bids[i+1];
        }
        delete bids[bidsLength.current()-1];
        bidsLength.decrement();
    }

    function _removeOffer(uint index)  public {
        require(index < offersLength.current(), "wrong lenght");

        for (uint i = index; i<offersLength.current()-1; i++){
            offers[i] = offers[i+1];
        }
        delete offers[offersLength.current()-1];
        offersLength.decrement();
    }
 
}