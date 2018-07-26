from yandex_speech import TTS

#Yandex Speechkit
def t_to_s(text):
	tts = TTS("oksana", "opus", "b04291f2-5e31-4c8e-af57-1695b7bd5f16")
	tts.generate(text)
	tts.save("ramazan")
	return "ramazan"

t_to_s("Привет! Меня зовут Оксана. А как зовут тебя?")