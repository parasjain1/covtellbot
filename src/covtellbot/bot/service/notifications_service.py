from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import bot.commons as bot_commons
from bot.dao.subscriptions_dao import get_all_subscriptions
from commons.constants import ANY_PINCODE


def send_notifications(center, message, session_id):
    reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("Book Slot", callback_data=f"book/{session_id}")
            ]])
    for chat_id, pincodes in get_all_subscriptions():
        if ANY_PINCODE in set(pincodes):
            bot_commons.updater.bot.sendMessage(chat_id, message, reply_markup=reply_markup)
        elif str(center.get('pincode')) in set(pincodes):
            bot_commons.updater.bot.sendMessage(
                chat_id, f"[{center.get('pincode')}] {message})", reply_markup=reply_markup
            )
