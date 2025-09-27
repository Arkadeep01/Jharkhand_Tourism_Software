import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-ethers";
import "@nomicfoundation/hardhat-toolbox";
import "dotenv/config";


const BLOCKCHAIN_RPC_URL = process.env.BLOCKCHAIN_RPC_URL || "";
const BLOCKCHAIN_PRIVATE_KEY = process.env.BLOCKCHAIN_PRIVATE_KEY || "";
const BLOCKCHAIN_CHAIN_ID = process.env.BLOCKCHAIN_CHAIN_ID
  ? parseInt(process.env.BLOCKCHAIN_CHAIN_ID)
  : 80001;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || "";
// const PAYMENT_PROOF_CONTRACT = process.env.PAYMENT_PROOF_CONTRACT || "";

const config: HardhatUserConfig = {
  solidity: {
    compilers: [
      {
        version: "0.8.28",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
    ],
  },
  networks: {
    hardhat: {
      type: "edr-simulated",
      chainType: "l1",
      chainId: 31337,
    },
    mumbai: {
      type: "http", 
      url: BLOCKCHAIN_RPC_URL,
      accounts: BLOCKCHAIN_PRIVATE_KEY ? [BLOCKCHAIN_PRIVATE_KEY] : [],
      chainId: BLOCKCHAIN_CHAIN_ID,
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY, 
  },
  mocha: {
    timeout: 20000,
  },
};

export default config;
