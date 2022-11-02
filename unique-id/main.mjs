import { Account, constants, Contract, Provider } from "starknet";
import { getKeyPair } from "starknet/dist/utils/ellipticCurve";
import * as implementationAbi from "./build/implementation_v1.json";

let uuid = "f6176a03-6993-4ca9-9c5f-2a9424e12daf";
//////// NOTICE: This does not include an uuid ////////
let baseUrl = "http://18.157.198.111:5052";

const provider = new Provider({
  sequencer: {
    baseUrl: `${baseUrl}`,
    chainId: constants.StarknetChainId.TESTNET,
    feederGatewayUrl: `${baseUrl}/feeder_gateway`,
    gatewayUrl: `${baseUrl}/gateway`,
    headers: {
      Authorization: `Basic ${Buffer.from(uuid + ":").toString("base64")}`,
    },
  },
});

const accountAddress =
  "0x6d9a6a4f4130bc724f0ba2954ff943fe658d43ca028235e3abc238f975995db";
const privateKey = "0xe229b833ebdc6064b936edaee8328729";
const account = new Account(provider, accountAddress, getKeyPair(privateKey));
const contractAddress =
  "0x33e4311c2d6c73f76db02d856535a84774404347edb945423effb27aeaf733b";
Contract(implementationAbi, contractAddress, account);

async function main() {
  let block = await provider.getBlock(0);

  account.invokeFunction();
  console.log(block);
}

main();
