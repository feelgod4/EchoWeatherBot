import config
import telebot
import pyowm
from pyowm.utils.config import get_config_from

bot = telebot.TeleBot(config.token)
owm = pyowm.OWM(api_key = config.weather_token, config = get_config_from("config_weather.json"))

@bot.message_handler(commands=['start'])
def start_message(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Привет, {name} \nЯ - эхо-бот твоих сообщений, а также могу показать прогноз погоды.\nЕсли хочешь его получить, пропиши /weather")

@bot.message_handler(commands=['weather'])
def command_weather(message):
        msg = bot.send_message(message.chat.id,'Какой город вас интересует?')
        bot.register_next_step_handler(msg, message_weather)

@bot.message_handler(commands=['info'])
def command_weather(message):
        msg = bot.send_message(message.chat.id,'/start - команда для запуска бота\n/weather - получить прогноз погоды в интересующем вас городе')

@bot.message_handler(content_types=["text"])
def repeat_text_messages(message):
    bot.send_message(message.chat.id, message.text)

@bot.message_handler(content_types = ['photo'])
def repeat_photo_messages(message):
    bot.send_photo(message.chat.id, message.photo[0].file_id, message.caption)

@bot.message_handler(content_types = ['sticker'])
def repeat_sticker_messages(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)

@bot.message_handler(content_types = ['audio'])
def repeat_audio_messages(message):
    bot.send_audio(message.chat.id, message.audio.file_id)

@bot.message_handler(content_types = ['voice'])
def repeat_voice_messages(message):
    bot.send_voice(message.chat.id, message.voice.file_id)

@bot.message_handler(content_types = ["text"])
def message_weather(message):
    try:
        observation = owm.weather_manager().weather_at_place(message.text)
        w = observation.weather
        detailed_temp = w.temperature(unit = 'celsius')

        answer = f"Погода {message.text}\n\nСейчас {w.detailed_status}\n"
        answer += f"Температура в районе {round(detailed_temp['temp'])}°C, ощущается как {round(detailed_temp['feels_like'])}°C\n\n"

        if detailed_temp['feels_like'] < 0:
            answer += 'Не забудь надеть шапку))'
        elif detailed_temp['feels_like'] < 15:
            answer += 'Прохладно, лучше приоденься'
        else:
            answer += 'Вперед навстречу приключениям'

        bot.send_message(message.chat.id, answer)
    except Exception:
        msg = bot.send_message(message.chat.id, "Информации о таком городе нет, попробуйте еще раз")
        bot.register_next_step_handler(msg, message_weather)

if __name__ == '__main__':
     bot.polling(none_stop=True)