// SPDX-License-Identifier: MIT
pragma solidity ^0.8.12;

import "./openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "./openzeppelin/contracts/utils/Counters.sol";

/// @title ERC1155 token for energy tokenization
/// @author Pietro Piccini
/// @notice This contract allows energy providers to create tokens representing the energy they want to sell
/// @dev This contract is still in an experimental phase
contract EnergyToken is ERC1155{
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    //owner of the contract
    address public energyProvider;

    //mapping that maps enrgy amount --> tokeknID
    mapping(uint  => uint ) public energyToToken;


/// @author Pietro Piccini
/// @notice This constructor will initialize a new contract 
/// @param url the url pointing to the JSON description of the energy source
/// @dev The url is shared among all tokens minted in this contract, so the metadata is specific to each EnergyToken contract
    constructor(string memory url) ERC1155(url) {
        energyProvider = msg.sender;
    }


/// @notice This function is used to mint a batch of energy tokens
/// @param _energy the amount of energy (in kilowatts) that each token represents
/// @param _amount the amount of total tokes that will be minted
/// @dev for now i use a enregy to tokenID mapping but it could make sense to have the energy amount == tokenID such that the energy that it represents can be viewed in the envent emitted.
    function addEnergyBatch(uint _energy, uint _amount) external {
        require(_isApprovedOrOwner(energyProvider,msg.sender), "not approved");
        
        if(energyToToken[_energy] == 0){
            _tokenIdCounter.increment();
            energyToToken[_energy] = _tokenIdCounter.current();
        }
        _mint(msg.sender,energyToToken[_energy], _amount, "");
    }



/// @notice This function is used to check if the account trying to mint new token is authorized
/// @param _account the amount of energy (in kilowatts) that each token represents
/// @param _operator the amount of total tokes that will be minted
/// @dev for now it checks weather the _operator is ether the owner of the contract itself or is authorized by the owner
/// @return  true if _operator is authorized, false otherwise
    function _isApprovedOrOwner( address _account, address _operator) internal view returns(bool){
        if((_operator == energyProvider) || (isApprovedForAll(_account, _operator))){
            return true;
        }
        return false;
    }
    


    function _EnergyTokenAvailable(uint _energyAmount) external view returns(bool){
        if(energyToToken[_energyAmount] == 0){
            return false;
        }
        else{
            return true;
        }
    }
}
