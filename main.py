import asyncio
import inspect
from loguru import logger
from modules.provider import get_module


async def run_option(methods: list):
    for method in methods:
        if callable(method):
            if inspect.iscoroutinefunction(method):
                await method()
            else:
                method()
        else:
            print(f"Object {method} is not callable")


def greeting_message():
    start_message = r'''        
    Modules:
    1: generate_wallets                                  | Generate ArgentX wallets and export wallets data to Excel file
    2: deploy_wallets                                    | Deploy ArgentX wallets
    0: exit                                              | Exit
    '''
    logger.debug(start_message)


async def startup():
    try:
        while True:
            greeting_message()
            module = input("Module: ")
            if not module.isdigit():
                logger.error("Wrong module format. It should be number")

            if module == "0":
                logger.info("Shutting down. Bye!")
            else:
                logger.info(f"Start module {module}")

            worker = get_module(module)
            if not worker:
                logger.error("Wrong module number")

            await run_option(worker)

    except Exception as e:
        logger.error(e)


asyncio.run(startup())
