# _*_ coding: utf-8 _*_
from xml.etree import ElementTree
import requests
import uuid

YANDEX_KEY = 'b04291f2-5e31-4c8e-af57-1695b7bd5f16'
VOICE_LANGUAGE = 'ru-RU'
MAX_MESSAGE_SIZE = 1000 * 50
MAX_MESSAGE_DURATION = 60


def speechapp(filename):
    data = open(filename, 'rb')
    txt = ""
    xml_data = requests.post(
        "https://asr.yandex.net/asr_xml?uuid={}&key={}&topic={}&lang={}".format(
            uuid.uuid4().hex,
            YANDEX_KEY,
            'queries',
            VOICE_LANGUAGE
        ),
        data=data,
        headers={"Content-type": 'audio/ogg;codecs=opus'}
    ).content

    e_tree = ElementTree.fromstring(xml_data)

    if not int(e_tree.attrib.get('success', '0')):
        txt = "Говорите кратко и ясно, а то Вас плохо слышно!"
        return txt

    txt = e_tree[0].text
    if ('<censored>' in txt) or (not txt):
        txt = "Не понял, пожалуйста повторите!"
        return txt
    return txt


print(speechapp("ramazan.opus"))
