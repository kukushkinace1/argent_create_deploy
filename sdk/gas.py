import time

from loguru import logger
from web3 import Web3

from constants import ETH_MAINNET_RPC


def get_eth_gas_fee():
    w3 = Web3(Web3.HTTPProvider(ETH_MAINNET_RPC))
    return w3.from_wei(w3.eth.gas_price, 'gwei')


def wait_for_gas(max_gvei):
    """Проверяем и ждем низкий газ"""

    cur_gas = get_eth_gas_fee()
    if cur_gas > max_gvei:
        logger.warning(f"Current gas '{cur_gas}' gwei is too high. Waiting for low gas...")
        while True:
            time.sleep(30)
            if get_eth_gas_fee() < max_gvei:
                logger.warning(f"Current gas '{cur_gas}' gwei is norm. Let's go working!")
                break



