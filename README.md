
# BDASnackBot
Simple bot to keep track of snacks and beers debts.

## Installation
Replace DATABASE_URL, API_TOKEN, URL, PRICE_UNIT in [bot.py](bot.py) to suit your needs.

### Heroku deployment
Clone the repo, create a PostgreSQL database with a 'debt' table with two columns: 'userid' and 'balance'.
Generate a Telegram API token with [@BotFather](https://telegram.me/BotFather).
Add the 2 following config vars:
* API_TOKEN: the previously generated token
* URL: your app url

## Usage
Add the bot to your group chat, then:
* Writing +1 in chat: adds 1 snack/beer to your debt
* Writing -1 in chat: takes 1 snack/beer from your debt
* /start - Starts the bot
* /balance - Displays the debt of the current member
* /balance_bda - Displays the debt of each member
* /plus - Same as +1
* /moins - Same as -1

> 💜 Visionneirb - BDA ENSEIRB-MATMECA 2019/2020 💜
