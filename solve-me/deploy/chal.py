from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starkware.python.utils import to_bytes


async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying solve-me")
    storage_deploy = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/solve-me.json").read_text(),
        constructor_args=[],
    )
    await storage_deploy.wait_for_acceptance()

    return storage_deploy.deployed_contract.address


async def checker(
    client: AccountClient, intro_contract: Contract, player_address: int
) -> bool:
    solution = (await intro_contract.functions["is_solved"].call()).res

    return solution == 1
