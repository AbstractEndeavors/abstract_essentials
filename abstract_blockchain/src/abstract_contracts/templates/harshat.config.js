require("@nomiclabs/hardhat-waffle");
require('dotenv').config()
require("@nomiclabs/hardhat-web3");
require("@nomiclabs/hardhat-etherscan");
//require("hardhat-gas-reporter");
// This is a sample Hardhat task. To learn how to create your own go to
// https://hardhat.org/guides/create-task.html
task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();

  for (const account of accounts) {
    console.log(account.address);
  }
});
const Web3 = require('web3');

let web3 = new Web3('ws://localhost:8546');
console.log(web3);

const getHDWallet = () => {
  const { MNEMONIC, privateKey } = process.env;
  if (MNEMONIC && MNEMONIC !== "") {
    return {
      mnemonic: MNEMONIC,
    }
  }
  if (privateKey && privateKey !== "") {
    return [privateKey]
  }
  throw Error("Private Key Not Set! Please set up .env");
}

module.exports = {
defaultNetwork: "FUJI_avax",
etherscan: {
    apiKey: {
      avalancheFujiTestnet: 'G8N1PH6Y9X7U6FH3HB4D3RNNSTRCQNIEHG'
    }
  },

  solidity: {
    compilers: [
    	{
	version: "^^^*killMe*^^^",
	settings: {
		optimizer: {
	enabled: true,
	runs: 200
	}
	}
	},

    ],
  },
  	//gasLimit: 500000000,
      	//gas: 100,
      	//gasPrice: 25000000000
  networks: {
    "FUJI_avax":{
       url: "https://api.avax-test.network/ext/bc/C/rpc",
       apiKey: 'G8N1PH6Y9X7U6FH3HB4D3RNNSTRCQNIEHG',
       accounts: getHDWallet(),
	gasLimit: 500000000,
      	gas: 100,
      	gasPrice: 25000000000
      	
    },
    "fantom":{
       url: "https://rpcapi.fantom.network",
       accounts: getHDWallet(),
    },    
    "local-devnode": {
       url: "http://localhost:8545",
       accounts: getHDWallet(),
       
    },
    "fantom-test":{
    	url:"https://rpc.testnet.fantom.network/",
        accounts: getHDWallet(),
       
    },	
    "optimistic-kovan": {
       url: "https://kovan.optimism.io",
       accounts: getHDWallet(),
	gasLimit: 500000000,
      	gas: 100,
      	gasPrice: 10000

    },
    "optimism": {
       url: "https://mainnet.optimism.io",
       accounts: getHDWallet(),
    }
  }
};
