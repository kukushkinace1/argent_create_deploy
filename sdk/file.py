import json
import pandas as pd

from loguru import logger


def read_from_json(file_path, mute_on_error = False):
    try:
        with open(file_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError as e:
        logger.error(f"{str(e)} while try to open \"{file_path}\"") if not mute_on_error else None
    except Exception as e:
        logger.error(f"{str(e)} while open json file: \"{file_path}\"") if not mute_on_error else None


def read_from_excel(file_path, mute_on_error=False):
    try:
        excel_data = pd.read_excel(file_path)
        data = pd.DataFrame(excel_data, columns=('address', 'private_key', 'seed'))
        acc_list = []
        for v in data.values:
            acc_obj = {
                'address': v[0].strip(),
                'private_key': v[1].strip(),
                'seed': v[2].strip()
            }
            acc_list.append(acc_obj)
        return acc_list
    except FileNotFoundError as e:
        logger.error(f"{str(e)} while try to open \"{file_path}\"") if not mute_on_error else None
    except Exception as e:
        logger.error(f"{str(e)} while open xlsx file: \"{file_path}\"") if not mute_on_error else None


def write_to_json(file_path, data, mute_on_error = False):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=5)
    except FileNotFoundError as e:
        logger.error(f"{str(e)} while try to open \"{file_path}\"") if not mute_on_error else None
    except Exception as e:
        logger.error(f"{str(e)} while write to txt file: \"{file_path}\"") if not mute_on_error else None
