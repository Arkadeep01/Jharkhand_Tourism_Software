/// <reference types="hardhat/types/config" />
/// <reference types="hardhat/types/runtime" />

import "hardhat/types/runtime";
import { ethers as hardhatEthers } from "hardhat";

declare module "hardhat/types/runtime" {
  interface HardhatRuntimeEnvironment {
    ethers: typeof hardhatEthers;
  }
}
declare module "hardhat/types/config" {
  interface HardhatUserConfig {
    etherscan?: {
      apiKey?: string;
    };
    mocha?: {
      timeout?: number;
    };
  }

  interface HardhatConfig {
    etherscan: {
      apiKey: string;
    };
    mocha: {
      timeout: number;
    };
  }
}
