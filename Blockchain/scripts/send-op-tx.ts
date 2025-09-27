const hre = require("hardhat");

async function main() {
  const [sender] = await hre.ethers.getSigners();

  console.log("Sending transaction using the OP chain type");
  console.log("Sending 1 wei from", sender.address, "to itself");

  const tx = await sender.sendTransaction({
    to: sender.address,
    value: 1n,
  });

  await tx.wait();
  console.log("Transaction sent successfully");
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
