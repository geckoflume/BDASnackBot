import telebot

bot = telebot.TeleBot("API_KEY")


def full_username(user):
    return ' '.join(filter(None, [user.first_name, user.last_name]))


def plus(message):
    bot.reply_to(
        message, "Ajouté 1 snack/bière à votre dette, " +
        full_username(message.from_user) + " !")
    print("+1 pour", message.from_user.id)


def moins(message):
    bot.reply_to(
        message, "Enlevé 1 snack/bière à votre dette, " +
        full_username(message.from_user) + " !")
    print("-1 pour", message.from_user.id)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "💜 *Visionneirb - BDA ENSEIRB-MATMECA 2019/2020* 💜",
                 parse_mode="Markdown")


@bot.message_handler(commands=['balance', 'dette', 'total'])
def send_balance(message):
    bot.send_message(message.chat.id, "Votre balance : ")


@bot.message_handler(commands=['plus'])
def more(message):
    plus(message)


@bot.message_handler(commands=['moins'])
def less(message):
    moins(message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "+1" in message.text:
        plus(message)
    elif "-1" in message.text:
        moins(message)


bot.polling()
