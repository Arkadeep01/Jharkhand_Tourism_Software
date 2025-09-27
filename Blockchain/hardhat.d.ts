import "hardhat/types/config";

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
