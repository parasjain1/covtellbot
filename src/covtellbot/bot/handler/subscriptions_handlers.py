import datetime
import threading

from telegram import Update
from telegram.ext import CallbackContext

from bot.dao.subscriptions_dao import remove_all_subscriptions, create_subscription_for_pincode, \
    create_subscription_for_all
from commons.utils import get_logger

logger = get_logger(__name__)


def register_notify(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.message.chat_id)
    message = "Awesome! You'll start getting notifications for {}"
    if len(context.args) != 0:
        target = create_subscription_for_pincode
        args = (chat_id, context.args)
        message = message.format("specified pincodes")
    else:
        target = create_subscription_for_all
        args = (chat_id, )
        message = message.format(" all districts in Delhi. To receive only pincode specific notifications first unsubscribe by /stop and then subscribe again.")
    threading.Thread(target=target, args=args).start()
    update.message.reply_text(message)
    logger.info(f"Chat ID {chat_id} registered at UTC {datetime.datetime.utcnow()}")


def unregister_notify(update: Update, _: CallbackContext) -> None:
    chat_id = str(update.message.chat_id)
    threading.Thread(target=remove_all_subscriptions, args=(chat_id, )).start()
    update.message.reply_text("Done! You'll no longer get notifications.")
    logger.info(f"Chat ID {chat_id} unregistered at UTC {datetime.datetime.utcnow()}")



