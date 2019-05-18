import os
import telebot
import psycopg2
from flask import Flask, request

DATABASE_URL = os.environ['DATABASE_URL']
API_TOKEN = os.environ['API_TOKEN']
URL = os.environ['URL']
PRICE_UNIT = 0.5

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)


def full_username(user):
    return ' '.join(filter(None, [user.first_name, user.last_name]))


def get_balance(userid):
    cur.execute("SELECT * FROM debts WHERE userid=%s;", [userid])
    ret = 0
    if cur.rowcount > 0:
        ret = cur.fetchone()[1]
    return ret


def get_balance_str(userid):
    return str(get_balance(userid)) + " 🍫"


def plus(message):
    cur.execute(
        "INSERT INTO debts (userid, balance) VALUES (%s, 1) ON CONFLICT (userid) DO UPDATE SET balance = debts.balance + 1;",
        [message.from_user.id])
    conn.commit()
    bot.reply_to(message,
                 "Ajouté 1 🍫 à votre dette, " +
                 full_username(message.from_user) + " !\n*Dette actuelle :* " +
                 get_balance_str(message.from_user.id),
                 parse_mode='Markdown')


def moins(message):
    cur.execute(
        "INSERT INTO debts (userid, balance) VALUES (%s, 1) ON CONFLICT (userid) DO UPDATE SET balance = debts.balance - 1;",
        [message.from_user.id])
    conn.commit()
    bot.reply_to(message,
                 "Enlevé 1 🍫 de votre dette, " +
                 full_username(message.from_user) + " !\n*Dette actuelle :* " +
                 get_balance_str(message.from_user.id),
                 parse_mode='Markdown')


def total():
    cur.execute("SELECT SUM (balance) FROM debts;")
    ret = 0
    if cur.rowcount > 0:
        ret = int(cur.fetchone()[0])
    return ret


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "💜 *Visionneirb - BDA ENSEIRB-MATMECA 2019/2020* 💜",
                 parse_mode='Markdown')


@bot.message_handler(commands=['balance'])
def send_balance(message):
    bot.send_message(message.chat.id,
                     "Votre dette : " + get_balance_str(message.from_user.id))


@bot.message_handler(commands=['balance_bda'])
def send_balance_bda(message):
    sum = total()
    cur.execute("SELECT * FROM debts ORDER BY balance DESC;")
    i = 0

    res = "*Dettes de " + str(cur.rowcount) + " membre"
    if cur.rowcount > 1:
        res += "s"
    res += "* (total : " + str(sum) + "x" + "{:.2f}".format(
        PRICE_UNIT) + "=" + "{:.2f}".format(sum * PRICE_UNIT) + "€) :\n"
    for row in cur.fetchall():
        i += 1
        u = bot.get_chat_member(message.chat.id, row[0]).user
        res += str(i) + " - " + full_username(u)
        if u.username is not None:
            res += " (@" + u.username + ")"
        res += " : " + str(row[1]) + " 🍫" + "\n"
    bot.send_message(message.chat.id, res, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "+1" in message.text:
        plus(message)
    elif "-1" in message.text:
        moins(message)


@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "VZ <3", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + API_TOKEN)
    return "VZ <3", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

print("Bot started successfully!")
