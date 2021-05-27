from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackContext, CallbackQueryHandler, \
    ConversationHandler, MessageHandler, Filters

from bot.handler.booking_workflow_handlers import handle_start_booking, exit_booking_convo, INPUT_PHONE, \
    handle_input_phone, INPUT_OTP, handle_input_otp
from bot.handler.common_handlers import start
from bot.handler.subscriptions_handlers import unregister_notify, register_notify
from commons.constants import DOWNSTREAM_ENABLED, BOT_TOKEN

updater = None
dispatcher = None


def init_bot():
    global updater
    global dispatcher
    if DOWNSTREAM_ENABLED:
        # Create the Telegram Updater and Dispatcher
        updater = Updater(BOT_TOKEN)
        # Get the dispatcher to register handler
        dispatcher = updater.dispatcher
        # on different commands - answer in Telegram
        dispatcher.add_handler(ConversationHandler(
            entry_points=[CallbackQueryHandler(handle_start_booking, pattern="book/")],
            states={
                INPUT_PHONE: [
                    MessageHandler(
                        Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                        handle_input_phone,
                    )
                ],
                INPUT_OTP: [
                    MessageHandler(
                        Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                        handle_input_otp,
                    )
                ]
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), exit_booking_convo)]
        ))
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("stop", unregister_notify))
        dispatcher.add_handler(CommandHandler("notify", register_notify))
        updater.start_polling()
