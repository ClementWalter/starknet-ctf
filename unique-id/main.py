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

uuid = "d2e58f66-215a-488f-a9d9-c636778c6ad2"
endpoint = "http://d2e58f66-215a-488f-a9d9-c636778c6ad2@18.157.198.111:5052"
private_key = "0xce660119839106e693f24193007db1a8"
player_address = "0x1a2bdbd6cc2c0b1f77b3016d98cc39f95addc89caab03eec094d0f85bc7f9d1"
contract_address = "0x2072a016bfccb1525c74a963af355863afc36791016c50abdf6723cc9c00624"

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
    proxy_abi = json.load(open("unique-id/build/proxy.json"))["abi"]
    contract = Contract(contract_address, proxy_abi, account_client)

    implementation_abi = json.load(open("unique-id/build/implementation_v1.json"))[
        "abi"
    ]
    wrapped_contract = Contract(
        address=contract_address, abi=implementation_abi, client=account_client
    )

    await contract.functions["get_is_owner"].call(player_address)

    tx = await wrapped_contract.functions["mintNewId"].invoke(1, 1, max_fee=int(1e16))
    await tx.wait_for_acceptance()

    await contract.functions["get_is_owner"].call(player_address)

    implementation_v1_deployment = await Contract.deploy(
        client=account_client,
        compiled_contract=Path("unique-id/build/implementation_v1.json").read_text(),
        constructor_args=[],
        salt=111111,
    )
    await implementation_v1_deployment.wait_for_acceptance()

    new_implementation_hash = await gateway_client.get_class_hash_at(
        implementation_v1_deployment.deployed_contract.address
    )

    tx = await contract.functions["upgrade"].invoke(
        new_implementation_hash, max_fee=int(1e16)
    )

    await tx.wait_for_acceptance()

    player_id = (
        await wrapped_contract.functions["getIdNumber"].call(player_address)
    ).id_number


if __name__ == "__main__":
    asyncio.run(run())
