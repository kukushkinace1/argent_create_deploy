import random
import time
from datetime import datetime
from sys import stderr
from loguru import logger
from progress.bar import IncrementalBar
from starknet_py.net.client_errors import ClientError
from starknet_py.net.signer.stark_curve_signer import KeyPair

from config import WALLETS_EXCEL_PATH, DEPLOY_SLEEP_DEVIATION_IN_SEC, \
    CLIENT_ON_ERROR_SLEEP_IN_SEC, CLIENT_ON_ERROR_TOTAL_TRIES
from models.wallet import Wallet
from sdk.deploy_wallet import DeployWallet
from sdk.file import read_from_excel

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <3}</level> | <level>{message}</level>")

class DeployWallets:
    @staticmethod
    def get_deploy_sleep_time():
        return random.randint(*DEPLOY_SLEEP_DEVIATION_IN_SEC)

    @staticmethod
    async def deploy():
        logger.info("Running deploy ArgentX wallets")
        deployer = DeployWallet()
        generated_wallets = read_from_excel(WALLETS_EXCEL_PATH)

        current_deploy_failed_wallets = list()
        current_deploy_success_wallets = list()

        current_deploy_wallets = []
        if isinstance(generated_wallets, list):
            current_deploy_wallets.extend(generated_wallets)

        logger.info(f"Total wallets for deploy: {len(current_deploy_wallets)}")
        bar = IncrementalBar('Deployed wallets', max=len(current_deploy_wallets))
        for index, wallet_json in enumerate(current_deploy_wallets, 1 - len(current_deploy_wallets)):
            wallet = Wallet(**wallet_json)
            key_pair = KeyPair.from_private_key(int(wallet.private_key, 16))

            deploy_attempt = 1
            while True:
                try:
                    if deploy_attempt > CLIENT_ON_ERROR_TOTAL_TRIES:
                        logger.info("Reached maximum attempts for wallet deploy. Skipping")
                        current_deploy_failed_wallets.append(wallet_json)
                        break

                    logger.info(f"Running deploy for wallet {wallet.address}. Attempt {deploy_attempt}")
                    is_deployed = await deployer.deploy(
                        key_pair,
                        wallet.address
                    )
                    if not is_deployed:
                        current_deploy_failed_wallets.append(wallet_json)
                        break
                    else:
                        bar.next()
                        current_deploy_success_wallets.append(wallet.address)
                        break
                except ClientError as e:
                    logger.error(
                        f"Starknet client error. Sleeping for {CLIENT_ON_ERROR_SLEEP_IN_SEC}sec. Trying another attempt")
                except Exception as e:
                    logger.error(
                        f"Unexpected error {e}. Sleeping for {CLIENT_ON_ERROR_SLEEP_IN_SEC}sec. Trying another attempt"
                    )
                finally:
                    deploy_attempt = deploy_attempt + 1
                    time.sleep(CLIENT_ON_ERROR_SLEEP_IN_SEC)

            if index:
                deploy_sleep = DeployWallets.get_deploy_sleep_time()
                logger.info(f"Sleeping before next deploy for {deploy_sleep}sec.")
                time.sleep(deploy_sleep)

        logger.info(
            f"All wallets were attempted to deploy. Failed: {len(current_deploy_failed_wallets)}. Success: {len(current_deploy_success_wallets)}")

        if len(current_deploy_success_wallets) != 0:
            current_deploy_success_wallets.insert(0, str(datetime.now()))
            current_deploy_success_wallets.append("")

        if len(current_deploy_failed_wallets) > 0:
            print(f"Failed deploy wallets:\n")
            for wal in current_deploy_failed_wallets:
                print(f"{wal.get('address')}")
