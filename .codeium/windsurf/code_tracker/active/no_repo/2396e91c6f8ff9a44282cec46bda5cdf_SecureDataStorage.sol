
Lc:/Users/Rohit3129/CascadeProjects/secure-data-storage/SecureDataStorage.solÙ// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureDataStorage {
    // Owner of the contract
    address private immutable owner;
    
    // Struct to store data with access control
    struct SecureData {
        bytes32 data;
        address owner;
        bool exists;
        mapping(address => bool) authorizedUsers;
    }
    
    // Mapping from ID to SecureData
    mapping(bytes32 => SecureData) private dataStore;
    
    // Events
    event DataStored(bytes32 indexed id, address indexed owner);
    event DataAccessed(bytes32 indexed id, address indexed accessor);
    event AccessGranted(bytes32 indexed id, address indexed user);
    event AccessRevoked(bytes32 indexed id, address indexed user);
    
    // Constructor
    constructor() {
        owner = msg.sender;
    }
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyDataOwner(bytes32 _id) {
        require(dataStore[_id].owner == msg.sender, "Only data owner can perform this action");
        _;
    }
    
    modifier hasAccess(bytes32 _id) {
        require(
            dataStore[_id].owner == msg.sender || 
            dataStore[_id].authorizedUsers[msg.sender],
            "Access denied"
        );
        _;
    }
    
    // Store new data
    function storeData(bytes32 _id, bytes32 _data) external {
        require(!dataStore[_id].exists, "Data ID already exists");
        
        SecureData storage newData = dataStore[_id];
        newData.data = _data;
        newData.owner = msg.sender;
        newData.exists = true;
        
        emit DataStored(_id, msg.sender);
    }
    
    // Retrieve data
    function getData(bytes32 _id) external view 
        hasAccess(_id) 
        returns (bytes32) 
    {
        require(dataStore[_id].exists, "Data does not exist");
        return dataStore[_id].data;
    }
    
    // Grant access to another user
    function grantAccess(bytes32 _id, address _user) external 
        onlyDataOwner(_id) 
    {
        require(_user != address(0), "Invalid address");
        require(!dataStore[_id].authorizedUsers[_user], "User already has access");
        
        dataStore[_id].authorizedUsers[_user] = true;
        emit AccessGranted(_id, _user);
    }
    
    // Revoke access from a user
    function revokeAccess(bytes32 _id, address _user) external 
        onlyDataOwner(_id) 
    {
        require(dataStore[_id].authorizedUsers[_user], "User does not have access");
        
        dataStore[_id].authorizedUsers[_user] = false;
        emit AccessRevoked(_id, _user);
    }
    
    // Check if user has access to data
    function hasDataAccess(bytes32 _id, address _user) external view 
        returns (bool) 
    {
        return dataStore[_id].owner == _user || dataStore[_id].authorizedUsers[_user];
    }
}
Ù2Tfile:///c:/Users/Rohit3129/CascadeProjects/secure-data-storage/SecureDataStorage.sol