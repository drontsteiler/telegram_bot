# _*_ coding: utf-8 _*_
from xml.etree import ElementTree
import requests
from telebot import TeleBot
import uuid
from api.texttospeech import  t_to_s

TELEGRAM_KEY = '650553991:AAG-0pMF9lZKkGLAB-GJZ-7sVMYluYcO6qc'
YANDEX_KEY = 'b04291f2-5e31-4c8e-af57-1695b7bd5f16'
VOICE_LANGUAGE = 'ru-RU'
MAX_MESSAGE_SIZE = 1000 * 50
MAX_MESSAGE_DURATION = 60
bot = TeleBot(TELEGRAM_KEY)
print("Start locale telegram bot")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=["voice"])
def voice_messages(message):
    data = message.voice
    bot.send_chat_action(message.chat.id, 'typing')
    if (data.file_size > MAX_MESSAGE_SIZE) or (data.duration > MAX_MESSAGE_DURATION):
        reply = ' '.join((
            "Голосовое сообщение слишком длинный.",
            "Максимальная длительность: {} сек.".format(MAX_MESSAGE_DURATION),
            "Постарайтесь говорить по короче.",
        ))
        return bot.reply_to(message, reply)
    file_url = "https://api.telegram.org/file/bot{}/{}".format(
        bot.token,
        bot.get_file(data.file_id).file_path
    )
    xml_data = requests.post(
        "https://asr.yandex.net/asr_xml?uuid={}&key={}&topic={}&lang={}".format(
            uuid.uuid4().hex,
            YANDEX_KEY,
            'queries',
            VOICE_LANGUAGE
        ),
        data=requests.get(file_url).content,
        headers={"Content-type": 'audio/ogg;codecs=opus'}
    ).content

    e_tree = ElementTree.fromstring(xml_data)

    if not int(e_tree.attrib.get('success', '0')):
        return bot.reply_to(message, "Говорите кратко и ясно, а то Вас плохо слышно!")

    text = e_tree[0].text
    print(text)
    if ('<censored>' in text) or (not text):
        return bot.reply_to(message, "Не понял, пожалуйста повторите!")

    if ('привет' in text) or ('как дела' in text):
        mess = "Привет! Как ваши дела?"
        t_to_s(mess)
        voice = open('ramazan.opus', 'rb')
        return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id, mess)

    if ('хорошо' in text) or ('сама' in text):
        t_to_s("Рада это слышать. У меня тоже все хорошо")
        voice = open('ramazan.opus', 'rb')
        return bot.send_voice(message.chat.id, voice)

    voice = open('ramazan.opus', 'rb')
    return bot.send_voice(message.chat.id, voice)


if __name__ == '__main__':
    bot.polling(none_stop=True)
