GENERATED_WALLETS_JSON_PATH = "data/generated_wallets.json"
WALLETS_EXCEL_PATH = "data/wallets.xlsx"



"""
       МОЖНО МЕНЯТЬ СНИЗУ     
"""

WALLETS_TO_GENERATE_COUNT = 2 # кол-во кошельков для генерации

DEPLOY_SLEEP_DEVIATION_IN_SEC = (10, 20) #время паузы между деплоями

CLIENT_ON_ERROR_TOTAL_TRIES = 3 #количество попыток после ошибки

CLIENT_ON_ERROR_SLEEP_IN_SEC = 10 #время паузы после ошибки

MAX_GWEI = 30 #контролер гвея
