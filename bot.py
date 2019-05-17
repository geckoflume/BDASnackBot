import telebot
import psycopg2

conn = psycopg2.connect("dbname=snacks user=bot password=password")
cur = conn.cursor()

bot = telebot.TeleBot("API_KEY")


def full_username(user):
    return ' '.join(filter(None, [user.first_name, user.last_name]))


def get_balance(userid):
    cur.execute("SELECT * FROM debts WHERE userid=%s;", [userid])
    ret = 0
    if cur.rowcount > 0:
        ret = cur.fetchone()[1]
    return ret


def get_balance_str(userid):
    return str(get_balance(userid)) + " snacks/bières"


def plus(message):
    cur.execute(
        "INSERT INTO debts (userid, balance) VALUES (%s, 1) ON CONFLICT (userid) DO UPDATE SET balance = debts.balance + 1;",
        [message.from_user.id])
    conn.commit()
    bot.reply_to(
        message, "Ajouté 1 snack/bière à votre dette, " +
        full_username(message.from_user) + " !\nDette actuelle : " +
        get_balance_str(message.from_user.id))


def moins(message):
    cur.execute(
        "INSERT INTO debts (userid, balance) VALUES (%s, 1) ON CONFLICT (userid) DO UPDATE SET balance = debts.balance - 1;",
        [message.from_user.id])
    conn.commit()
    bot.reply_to(
        message, "Enlevé 1 snack/bière de votre dette, " +
        full_username(message.from_user) + " !\nDette actuelle : " +
        get_balance_str(message.from_user.id))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "💜 *Visionneirb - BDA ENSEIRB-MATMECA 2019/2020* 💜",
                 parse_mode="Markdown")


@bot.message_handler(commands=['balance'])
def send_balance(message):
    bot.send_message(
        message.chat.id,
        "Votre balance : " + get_balance_str(message.from_user.id))


@bot.message_handler(commands=['balance_bda'])
def send_balance_bda(message):
    cur.execute("SELECT * FROM debts ORDER BY balance DESC;")
    res = "*Dettes de " + str(cur.rowcount) + " membre"
    if cur.rowcount > 1:
        res += "s"
    res += "*\n"
    for row in cur.fetchall():
        u = bot.get_chat_member(message.chat.id, row[0]).user
        res += "Balance de " + full_username(
            u) + " (@" + u.username + ") : " + str(
                row[1]) + " snacks/bières" + "\n"
    bot.send_message(message.chat.id, res, parse_mode="Markdown")


@bot.message_handler(commands=['plus'])
def more(message):
    plus(message)


@bot.message_handler(commands=['moins'])
def less(message):
    moins(message)


@bot.message_handler(func=lambda message: "+1" in message.text)
def echo_all(message):
    plus(message)


@bot.message_handler(func=lambda message: "-1" in message.text)
def echo_all(message):
    moins(message)


bot.polling()
