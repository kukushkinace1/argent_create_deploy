from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call

from constants import ETH_STARKNET_TOKEN_ADDRESS


async def check_account_balance(chain, client, address, key_pair):
    account = Account(
        address=address,
        key_pair=key_pair,
        chain=chain,
        client=client
    )

    call = Call(
        to_addr=ETH_STARKNET_TOKEN_ADDRESS,
        selector=get_selector_from_name("balanceOf"),
        calldata=[account.address],
    )

    return await account.client.call_contract(call)
