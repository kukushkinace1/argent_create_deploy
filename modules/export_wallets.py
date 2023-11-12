from loguru import logger

from config import WALLETS_EXCEL_PATH, GENERATED_WALLETS_JSON_PATH
from sdk.export_to_excel import export_to_one_sheet


class ExportWallets:
    @staticmethod
    def export():
        logger.info("Starting ArgentX exporter")
        export_to_one_sheet(GENERATED_WALLETS_JSON_PATH, WALLETS_EXCEL_PATH)
