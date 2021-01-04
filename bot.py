import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ку \nЯ - эхо-бот твоих сообщений, а также могу показать прогноз погоды')

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

if __name__ == '__main__':
     bot.polling(none_stop=True)
