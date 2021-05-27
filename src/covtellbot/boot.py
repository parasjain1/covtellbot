from bot.commons import init_bot
from bot.dao.subscriptions_dao import init_subscriptions
from commons.utils import get_logger
from slot_poller import start_polling

logger = get_logger(__name__)


if __name__ == "__main__":
    init_subscriptions()
    init_bot()
    start_polling()



