// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// @title PaymentProof - store SHA256 payment hashes (strings)
contract PaymentProof {
    event HashStored(address indexed sender, string indexed dataHash, uint256 timestamp);

    // Simple storage of hashes (optional)
    string[] public hashes;

    function storeHash(string calldata dataHash) external returns (bool) {
        hashes.push(dataHash);
        emit HashStored(msg.sender, dataHash, block.timestamp);
        return true;
    }

    function getHashCount() external view returns (uint256) {
        return hashes.length;
    }

    function getHash(uint256 idx) external view returns (string memory) {
        require(idx < hashes.length, "Index out of range");
        return hashes[idx];
    }
}
