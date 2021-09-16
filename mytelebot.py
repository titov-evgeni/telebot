import telebot
# from auth_data import token1
import pars_for_teleg as parsing
import json

bot = telebot.TeleBot("input your token")


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Введите команду /search для того,"
                                      " чтобы начать поиск вакансий")


@bot.message_handler(commands=['search'])
def input_text(message):
    msg = bot.send_message(message.chat.id,
                           "Введите текст, который вы хотите найти")
    bot.register_next_step_handler(msg, search)


def search(message):
    try:
        bot.send_message(message.chat.id, "Ищу...")
        response = json.loads(parsing.get_data(message.text))

        # parsing.get_data(message.text)
        # with open("all_categories_dict.json", encoding="utf-8-sig") as file:
        #     response = json.load(file)
        # file.close()

        for category_name, category_href in response.items():
            bot.send_message(
                message.chat.id,
                f"{category_name}\n{category_href}"
            )
        bot.send_message(message.chat.id, "Поиск окончен")
        input_text(message)
    except (Exception, ):
        bot.send_message(
            message.chat.id,
            "Черт...Что-то пошло не так..."
        )


bot.polling()
