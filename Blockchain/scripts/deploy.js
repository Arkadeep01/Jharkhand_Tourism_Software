async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);

  const PaymentProof = await ethers.getContractFactory("PaymentProof");
  const paymentProof = await PaymentProof.deploy();
  await paymentProof.deployed();

  console.log("PaymentProof deployed to:", paymentProof.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
