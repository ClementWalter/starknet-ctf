from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starkware.python.utils import to_bytes


async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying magic-encoding")
    bitwise_deployement = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/magic-encoding.json").read_text(),
        constructor_args=[],
    )
    await bitwise_deployement.wait_for_acceptance()
    return bitwise_deployement.deployed_contract.address


async def checker(
    client: AccountClient, bitwise_contract: Contract, player_address: int
) -> bool:
    solution = (await bitwise_contract.functions["is_challenge_done"].call()).res

    return solution == 1
