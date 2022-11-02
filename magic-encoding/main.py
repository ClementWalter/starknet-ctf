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

uuid = "556ebb03-58a5-4537-8e82-7bba1f207fa0"
endpoint = "http://556ebb03-58a5-4537-8e82-7bba1f207fa0@18.157.198.111:5050"
private_key = "0x8e8905af1c6d73dcd5bdeb3110f7ff9e"
player_address = "0x21c3981ff76660d70abc188e92d8898b9c6b64a9f3ef1e32d18f7cb970aae5d"
contract_address = "0x6f389521c3e1976e0146459ff1679a94f63f9c390c5e2e8c9b3f2cd2e6aa614"

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
    contract.data.abi

    passwords = [
        "0x480680017fff8000",
        "0x53746f7261676552656164",
        "0x400280007ffc7fff",
        "0x400380017ffc7ffd",
        "0x482680017ffc8000",
        "0x3",
        "0x480280027ffc8000",
        "0x208b7fff7fff7ffe",
        "0x480680017fff8000",
        "0x53746f726167655772697465",
        "0x400280007ffb7fff",
        "0x400380017ffb7ffc",
        "0x400380027ffb7ffd",
        "0x482680017ffb8000",
        "0x3",
        "0x208b7fff7fff7ffe",
        "0x400380007ffb7ffc",
        "0x400380017ffb7ffd",
        "0x482680017ffb8000",
        "0x5",
        "0x480280037ffb8000",
        "0x208b7fff7fff7ffe",
        "0x480a7ffc7fff8000",
        "0x480a7ffd7fff8000",
        "0x480680017fff8000",
        "0x3bd5999d9835e5a2497d76df48d4a46d7f221796ffcb7ce7f9155f10a5677e9",
        "0x208b7fff7fff7ffe",
        "0x480a7ffc7fff8000",
        "0x480a7ffd7fff8000",
        "0x1104800180018000",
        "0x800000000000010fffffffffffffffffffffffffffffffffffffffffffffffa",
        "0x480a7ffb7fff8000",
        "0x48127ffe7fff8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffe0",
        "0x48127ffe7fff8000",
        "0x48127ff57fff8000",
        "0x48127ff57fff8000",
        "0x48127ffc7fff8000",
        "0x208b7fff7fff7ffe",
        "0x480a7ffb7fff8000",
        "0x480a7ffc7fff8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffed",
        "0x480a7ffa7fff8000",
        "0x48127ffe7fff8000",
        "0x480a7ffd7fff8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffda",
        "0x48127ff67fff8000",
        "0x48127ff67fff8000",
        "0x208b7fff7fff7ffe",
        "0x480a7ffb7fff8000",
        "0x480a7ffc7fff8000",
        "0x480a7ffd7fff8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffe5",
        "0x208b7fff7fff7ffe",
        "0x40780017fff7fff",
        "0x1",
        "0x4003800080007ffc",
        "0x4826800180008000",
        "0x1",
        "0x480a7ffd7fff8000",
        "0x4828800080007ffe",
        "0x480a80007fff8000",
        "0x208b7fff7fff7ffe",
        "0x402b7ffd7ffc7ffd",
        "0x480280007ffb8000",
        "0x480280017ffb8000",
        "0x480280027ffb8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffee",
        "0x48127ffe7fff8000",
        "0x1104800180018000",
        "0x800000000000010fffffffffffffffffffffffffffffffffffffffffffffff1",
        "0x48127ff47fff8000",
        "0x48127ff47fff8000",
        "0x48127ffb7fff8000",
        "0x480280037ffb8000",
        "0x48127ffa7fff8000",
        "0x48127ffa7fff8000",
        "0x208b7fff7fff7ffe",
        "0x480a7ffc7fff8000",
        "0x480680017fff8000",
        "0x3039",
        "0x480a7ffd7fff8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffba",
        "0x482480017fff8000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffb422",
        "0x20680017fff7fff",
        "0xd",
        "0x480a7ff97fff8000",
        "0x480a7ffa7fff8000",
        "0x480a7ffb7fff8000",
        "0x480680017fff8000",
        "0x1",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffc7",
        "0x48127fe77fff8000",
        "0x480680017fff8000",
        "0x1",
        "0x208b7fff7fff7ffe",
        "0x480a7ff97fff8000",
        "0x480a7ffa7fff8000",
        "0x480a7ffb7fff8000",
        "0x48127ffa7fff8000",
        "0x480680017fff8000",
        "0x0",
        "0x208b7fff7fff7ffe",
        "0x40780017fff7fff",
        "0x1",
        "0x4003800080007ffc",
        "0x4826800180008000",
        "0x1",
        "0x480a7ffd7fff8000",
        "0x4828800080007ffe",
        "0x480a80007fff8000",
        "0x208b7fff7fff7ffe",
        "0x482680017ffd8000",
        "0x1",
        "0x402a7ffd7ffc7fff",
        "0x480280007ffb8000",
        "0x480280017ffb8000",
        "0x480280027ffb8000",
        "0x480280037ffb8000",
        "0x480280007ffd8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffd4",
        "0x48127ffd7fff8000",
        "0x1104800180018000",
        "0x800000000000010ffffffffffffffffffffffffffffffffffffffffffffffed",
        "0x48127ff37fff8000",
        "0x48127ff37fff8000",
        "0x48127ffb7fff8000",
        "0x48127ff37fff8000",
        "0x48127ffa7fff8000",
        "0x48127ffa7fff8000",
        "0x208b7fff7fff7ffe",
    ]
    for password in passwords:
        try:
            tx = await contract.functions["test_password"].invoke(
                int(password, 16), max_fee=int(1e16)
            )
            await tx.wait_for_acceptance()
            solved = (await contract.functions["is_challenge_done"].call()).res
            if solved == 1:
                break
        except:
            continue


if __name__ == "__main__":
    asyncio.run(run())
