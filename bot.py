import os
from telebot import types
import store
import telebot
from api.weather import weatherapp
from flask import Flask, request

TOKEN = store.token
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
print("_______________________________________________________________\n"
      + "Start Telegram Bot in file flask_bot.py" +
      "\n_______________________________________________________________")


########################################################################################################

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.from_user.id, "Welcome, " + message.from_user.first_name)


@bot.message_handler(commands=["stop"])
def handle_start(message):
    bot.send_message(message.chat.id, "..")


@bot.message_handler(content_types=["audio"])
def handle_audio(message):
    print("\n\nSending audio\n\n")
    bot.send_message(message.chat.id, "You send to me audio file!")


@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    print("\n\nSending voice messages\n\n")
    bot.send_message(message.chat.id, "You send to me voice messages!")
    file = open('audio/hello.ogg', 'rb')
    bot.send_voice(message.chat.id, file, None)


@bot.message_handler(content_types="text")
def handle_text(message):
    msg = "error"
    print("\n\nСообщение от пользователя:" + message.text + "\n\n")
    if message.text == "Что ты умеешь делать?":
        keyboard = types.InlineKeyboardMarkup()
        weather = types.InlineKeyboardButton(text="Погода", callback_data="weather")
        wikipedia = types.InlineKeyboardButton(text="Энциклопедия", callback_data="inline")
        translate = types.InlineKeyboardButton(text="Переводчик", callback_data="inline")
        currency = types.InlineKeyboardButton(text="Валюта", callback_data="inline")
        payment = types.InlineKeyboardButton(text="Платеж", callback_data="inline")
        keyboard.add(weather)
        keyboard.add(wikipedia)
        keyboard.add(translate)
        keyboard.add(currency)
        keyboard.add(payment)
        bot.send_message(message.chat.id, "Я могу делать следующие:", reply_markup=keyboard)
    else:
        msg = weatherapp(message.text)
        bot.send_message(message.chat.id, msg, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "weather":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Введите название города")
    elif call.inline_message_id:
        if call.data == "weather":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Введите название города")


############################################################################################################################

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://aibota.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
