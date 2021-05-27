# covtellbot
A Telegram Bot to give real time vaccination slot notifications

* Start up command 
  `python3 boot.py`
* Set envrionment variable `BOT_TOKEN` before running the app. Bot token is the API Token for your telegram bot and can be obtained from Bot Father https://t.me/botfather
* `subscriptions.json` file would store the list of `chat_ids` with the pincodes they're subscribed too. When users would send `/notify` or `/notify <pincode>`, this file shall be updated. If the file is removed/lost, all users will have to re-subscribe to the bot via `/notify` command.
* It is suggested to set up a bot only for a few number of districts (say not more than 10) to not get frequently blocked by the rate-limiting policy of CoWIN APIs.
