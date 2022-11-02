# Usage:
import asyncio
import json
import os
import subprocess
from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starkware.starknet.definitions.general_config import StarknetChainId
from starkware.starknet.public.abi import get_selector_from_name

uuid = "013a7170-22f2-4f82-a001-6b19ac76da7f"
endpoint = "http://013a7170-22f2-4f82-a001-6b19ac76da7f@18.157.198.111:5055"
private_key = "0x6b0b6ee12cf2428fc45f02a486be16e5"
player_address = "0x5b878b07f2f1ebf995c6476fc50989e6138107b93c1190d8ca0ee3b86b98754"
contract_address = "0x2297e4595013ccf418139a88567e8e8db00ace2da5ea7534dbc44671f51472"

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
    json.dump(contract.data.abi, open("dna.json", "w"))

    # Just check challenge is not done yet
    await contract.functions["is_challenge_done"].call()

    tx = await contract.functions["test_password"].invoke(17 * [0], max_fee=int(1e16))
    await tx.wait_for_acceptance()
    tx = await contract.functions["test_password"].invoke(17 * [67], max_fee=int(1e16))
    await tx.wait_for_acceptance()
    tx = await contract.functions["test_password"].invoke(17 * [71], max_fee=int(1e16))
    await tx.wait_for_acceptance()
    tx = await contract.functions["test_password"].invoke(17 * [84], max_fee=int(1e16))
    await tx.wait_for_acceptance()
    tx = await contract.functions["test_password"].invoke(17 * [65], max_fee=int(1e16))
    await tx.wait_for_acceptance()


if __name__ == "__main__":
    asyncio.run(run())
