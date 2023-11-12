from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

import config
import constants
from sdk.check_balance import check_account_balance
from sdk.gas import wait_for_gas


class DeployWallet:
    def __init__(self, network: str = "mainnet", chain: StarknetChainId = StarknetChainId.MAINNET):
        self.network = network
        self.chain = chain
        self.client = GatewayClient(net=network)

    async def deploy(self, key_pair: KeyPair, address):
        wait_for_gas(config.MAX_GWEI)
        acc_balance = await check_account_balance(self.chain, self.client, address, key_pair)
        if acc_balance[0] <= 500000000000000:
            logger.error(f"Wallet balance {address} is is too low for deploy")
            return False

        constructor_calldata = [
            key_pair.public_key,
            0
        ]

        account_deployment_result = await Account.deploy_account(
            address=int(address, 16),
            class_hash=constants.ACCOUNT_CLASS_HASH,
            salt=key_pair.public_key,
            key_pair=key_pair,
            client=self.client,
            chain=self.chain,
            constructor_calldata=constructor_calldata,
            auto_estimate=True,
        )

        logger.info(
            f"{constants.STARKSCAN_URL}/{hex(account_deployment_result.hash)}")
        if await account_deployment_result.wait_for_acceptance():
            logger.success(f"Wallet {address} successfully deployed")
            return account_deployment_result
        else:
            logger.error(f"Wallet {address} is failed to deploy")
            return False
