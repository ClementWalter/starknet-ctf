# Usage:
import asyncio
import json
import os
import subprocess
from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starknet_py.net.gateway_client import GatewayClient, InvokeFunction
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.transactions.deploy import make_deploy_tx
from starkware.starknet.definitions.general_config import StarknetChainId
from starkware.starknet.public.abi import get_selector_from_name

endpoint = "http://641374c2-4c7e-4563-a852-577179029db3@18.157.198.111:5053"
private_key = "0xf0e797b29544f0feab1e7fedaa39d8c2"
player_address = "0x791c7815d1dfa04cd182e88f49a8993bd02a66b70e105e66b89c416d66e630a"
contract_address = "0x77edb044edfb13f71f1b3f0b28f0d1db691f87048968d6403215452820a2ae5"

private_key = int(private_key, 16)
player_address = int(player_address, 16)


def int_to_uint256(value):
    low = value & ((1 << 128) - 1)
    high = value >> 128
    return {"low": low, "high": high}


async def run():

    gateway_client = GatewayClient(net=endpoint, chain=StarknetChainId.TESTNET)
    account_client = AccountClient(
        address=player_address,
        client=gateway_client,
        chain=StarknetChainId.TESTNET,
        key_pair=KeyPair.from_private_key(private_key),
        supported_tx_version=1,
    )

    contract = await Contract.from_address(contract_address, account_client)

    tx = await contract.functions["deposit"].invoke(3, int(10000))
    await tx.wait_for_acceptance()

    (await contract.functions["get_winner"].call()).address


if __name__ == "__main__":
    asyncio.run(run())
