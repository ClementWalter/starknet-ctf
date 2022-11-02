from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient


async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying bid")
    bid_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/bid.cairo").read_text(),
        constructor_args=[],
    )
    await bid_deployment.wait_for_acceptance()

    print("[+] creating bidders")
    bidder = 1
    attacker = 2

    print("[+] initializing contracts")
    response = await client.execute(
        calls=[
            bid_deployment.deployed_contract.functions["deposit"].prepare(
                bidder, int(1000)
            ),
            bid_deployment.deployed_contract.functions["deposit"].prepare(
                attacker, int(10)
            ),
            bid_deployment.deployed_contract.functions["bid"].prepare(
                bidder, int(1000)
            ),
        ],
        max_fee=int(1e16),
    )

    await client.wait_for_tx(response.transaction_hash)

    return bid_deployment.deployed_contract.address


async def checker(
    client: AccountClient, bid_contract: Contract, player_address: int
) -> bool:
    winner = (await bid_contract.functions["get_winner"].call()).address

    return winner == 2
