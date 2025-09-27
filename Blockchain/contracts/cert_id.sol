// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TourismCertificateNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;

    // Mapping certificate ID to tokenId
    mapping(string => uint256) public certIdToToken;

    event CertificateMinted(address recipient, string certId, uint256 tokenId);

    constructor() ERC721("JharkhandTourismCertificate", "JTC") {
        tokenCounter = 1;
    }

    function mintCertificate(
        address recipient,
        string memory certId,
        string memory tokenURI
    ) external onlyOwner returns (uint256) {
        uint256 tokenId = tokenCounter;
        _safeMint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);
        certIdToToken[certId] = tokenId;

        tokenCounter += 1;

        emit CertificateMinted(recipient, certId, tokenId);
        return tokenId;
    }

    function getTokenId(string memory certId) external view returns (uint256) {
        return certIdToToken[certId];
    }
}
