from .client import RightClient, login_using_env_and_get_client
import json
import os
from . import dir_config as dc

from .utils import *


def get_waiting_items():
    """
    returns list of (commit_hash, record_id)
    """
    items = []
    for name in os.listdir(dc.wait_dir):
        commit_hash = name

        json_info = read_json_file(os.path.join(dc.wait_dir, name))
        record_id = json_info['record_id']

        items.append((commit_hash, record_id))

    return items


def is_packaged(record: dict):
    return record['transactionId'] is not None


def do_fetch():

    client = login_using_env_and_get_client()

    for commit_hash, record_id in get_waiting_items():
        record = client.get_record(record_id)
        if is_packaged(record):
            write_json_to_file(record, path=os.path.join(
                dc.packaged_dir, commit_hash))
            os.remove(os.path.join(dc.wait_dir, commit_hash))
            print("packaged:", commit_hash)
        else:
            print("still not packaged:", commit_hash)
