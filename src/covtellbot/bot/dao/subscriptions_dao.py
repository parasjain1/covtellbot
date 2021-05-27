import json
import os
import time
from typing import List, Dict

from commons.constants import SUBSCRIPTIONS_FILE_PATH, ANY_PINCODE
from commons.utils import get_logger

logger = get_logger(__name__)

SUBSCRIPTIONS_WRITE_LOCK = False

# chat IDs to notify
subscriptions: Dict[str, List] = {}


def _persist_subscriptions():
    global SUBSCRIPTIONS_WRITE_LOCK
    while SUBSCRIPTIONS_WRITE_LOCK:
        time.sleep(1/2)
    SUBSCRIPTIONS_WRITE_LOCK = True
    with open(SUBSCRIPTIONS_FILE_PATH, 'w') as file:
        file.write(json.dumps(subscriptions))
    SUBSCRIPTIONS_WRITE_LOCK = False


def create_subscription_for_pincode(chat_id: str, pincodes: List[str]):
    if subscriptions.get(chat_id) is None:
        subscriptions[chat_id] = List.copy(pincodes)
        _persist_subscriptions()
    else:
        updated_pincodes = set(subscriptions.get(chat_id)).union(set(pincodes))
        subscriptions[chat_id] = list(updated_pincodes)
        _persist_subscriptions()


def create_subscription_for_all(chat_id: str):
    if subscriptions.get(chat_id) is None:
        subscriptions[chat_id] = [ANY_PINCODE]
        _persist_subscriptions()
    elif ANY_PINCODE not in set(subscriptions.get(chat_id)):
        subscriptions[chat_id].append(ANY_PINCODE)
        _persist_subscriptions()


def remove_all_subscriptions(chat_id: str):
    if chat_id in subscriptions:
        del subscriptions[chat_id]
        _persist_subscriptions()


def remove_subscriptions_by_pincode(chat_id: str, pincode: str):
    if chat_id in subscriptions:
        subscriptions.get(chat_id).remove(pincode)
        _persist_subscriptions()


def get_all_subscriptions():
    for chat_id, subscription_list in subscriptions.items():
        yield (chat_id, subscription_list)


def init_subscriptions():
    global subscriptions
    if os.path.exists(SUBSCRIPTIONS_FILE_PATH):
        try:
            with open(SUBSCRIPTIONS_FILE_PATH, 'r') as file:
                data = file.read()
                subscriptions = json.loads(data)
                logger.info(f"{len(subscriptions)} subscriptions loaded from file")
        except Exception as e:
            logger.exception(e)
