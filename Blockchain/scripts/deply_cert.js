async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying NFT contract with account:", deployer.address);

  const NFTContract = await ethers.getContractFactory("TourismCertificateNFT");
  const nft = await NFTContract.deploy();
  await nft.deployed();

  console.log("NFT Contract deployed at:", nft.address);
}

main()
  .then(() => process.exit(0))
  .catch((err) => { console.error(err); process.exit(1); });
