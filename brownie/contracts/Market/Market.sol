// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC20/ERC20.sol)
pragma solidity ^0.8.12;
import "./EnergyToken.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "./Node.sol";
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
contract Market is Node{
    using Counters for Counters.Counter;

    //event that is raised when an offer and a bid match
    event Match(uint price, uint amount, uint timesatmp, address bidAddress, address offerAddress);

    EnergyToken public energyToken;
    IERC20 public stableCoin;
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
    constructor(address stableCoinAddress,
     address energyTokenAddress, 
     address marketNode)
     Node(marketNode)
     {
        stableCoin = IERC20(stableCoinAddress);
        energyToken = EnergyToken(energyTokenAddress);
    }

    // energy providers will call this function sepcifying the price and a 
    // max amount of energy availabe to sell
    function receiveOffer(OfferOrBid memory offer) public{
        energyToken.produce(offer._address, offer.amount);
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
    function receiveBid(OfferOrBid memory bid) public {
        bool transferred = stableCoin.transferFrom(msg.sender, address(this), bid.price*bid.amount);
        require(transferred, "transferred of stablecoins failed");
        usdBalance[msg.sender] += bid.price*bid.amount;
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
            //energyToken.approve(bid._address, bid.amount);
            bool transferred = stableCoin.transfer(offer._address, bid.amount*bid.price);
            require(transferred, "stablecoin transfer failed");
            energyToken.transferFrom(offer._address, bid._address, bid.amount);
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


    function forward(OfferOrBid memory offerOrBid) override internal {

    }

 
}