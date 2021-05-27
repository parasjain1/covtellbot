from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /notify <pincode> or /notify to start receiving notifications. /stop to remove all subsriptions.')
