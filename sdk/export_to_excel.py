import pandas as pd
from loguru import logger

from sdk.file import read_from_json


def export_to_one_sheet(file_to_read, file_to_save):
    content = read_from_json(file_to_read)
    df = pd.DataFrame(content)

    df.to_excel(file_to_save, index=False, engine='openpyxl')

    logger.info(f"Data exported to {file_to_save}")
