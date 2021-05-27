import time

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import bot.commons as bot_commons
from bot.dao.subscriptions_dao import get_all_subscriptions
from commons.constants import ANY_PINCODE

from commons.utils import get_logger

logger = get_logger(__name__)


def send_notifications(center, message, session_id):
    for chat_id, pincodes in get_all_subscriptions():
        if ANY_PINCODE in set(pincodes):
            try:
                bot_commons.updater.bot.sendMessage(chat_id, message)
            except Exception as e:
                logger.exception(f"Exception while sending update to chat ID {chat_id}")
        else:
            for pincode in set(pincodes):
                if str(center.get('pincode')) in pincode:
                    try:
                        bot_commons.updater.bot.sendMessage(chat_id, f"({center.get('pincode')}) {message})")
                    except Exception as e:
                        logger.exception(f"Exception while sending update to chat ID {chat_id}")