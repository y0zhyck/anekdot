# -*- coding: utf-8 -*-
import telebot
import requests
import random
import logging
import os
import re

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация - ЗАМЕНИТЕ НА СВОИ ДАННЫЕ!
TOKEN = "TOken ID"
CHANNEL_ID = "channel name or ID"
TOPIC_ID = number channel (28856)
ADMIN_IDS = [Your ID]

bot = telebot.TeleBot(TOKEN)

class JokeGenerator:
    def __init__(self):
        self.gai_jokes = self.load_jokes_from_file('GAI.txt', self.get_default_gai_jokes())
        self.moto_jokes = self.load_jokes_from_file('MOTO.txt', self.get_default_moto_jokes())
        self.general_jokes = self.load_jokes_from_file('GENERAL.txt', self.get_default_general_jokes())
        
        logger.info(f"Загружено анекдотов: ГАИ - {len(self.gai_jokes)}, МОТО - {len(self.moto_jokes)}, ОБЩИЕ - {len(self.general_jokes)}")
    
    def load_jokes_from_file(self, filename, default_jokes):
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:
                    jokes = [line.strip() for line in file if line.strip() and not line.startswith('#')]
                
                if jokes:
                    logger.info(f"Загружено {len(jokes)} анекдотов из {filename}")
                    return jokes
                else:
                    logger.warning(f"Файл {filename} пустой, используются анекдоты по умолчанию")
                    return default_jokes
            else:
                logger.warning(f"Файл {filename} не найден, создан пустой файл")
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("# Добавляйте анекдоты по одному на строку\n")
                    file.write("# Пустые строки и строки начинающиеся с # игнорируются\n")
                return default_jokes
                
        except Exception as e:
            logger.error(f"Ошибка загрузки анекдотов из {filename}: {e}")
            return default_jokes
    
    def get_default_gai_jokes(self):
        return [
            "Останавливает гаишник машину: - Ваши права! - А за что? - А вы на красный свет проехали! - Да чтоб вы знали, у меня зрение 100%! - Хорошо, тогда проедьте еще раз...",
            "Сотрудник ГАИ останавливает водителя: - Вы знаете, что у вас задний фонарь не работает? - Да что вы! Я даже не знал, что выехал!",
        ]
    
    def get_default_moto_jokes(self):
        return [
            "Объявление: 'Продам мотоцикл. Не бит, не крашен. Просто папа женился, и мама сказала, что или он, или я.'",
            "Почему мотоциклисты не боятся дождя? Потому что они и так уже мокрые от слез счастья, когда едут.",
        ]
    
    def get_default_general_jokes(self):
        return [
            "Программист ставит чайник с водой на плиту, чтобы попить чаю. Ждет-ждет, не закипает. Посмотрел - а он забыл его включить.",
            "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25.",
        ]
    
    def reload_jokes(self):
        self.gai_jokes = self.load_jokes_from_file('GAI.txt', self.get_default_gai_jokes())
        self.moto_jokes = self.load_jokes_from_file('MOTO.txt', self.get_default_moto_jokes())
        self.general_jokes = self.load_jokes_from_file('GENERAL.txt', self.get_default_general_jokes())
        return True
    
    def get_joke_from_rzhunemogu(self, ctype=1):
        url = f"http://rzhunemogu.ru/RandJSON.aspx?CType={ctype}"
        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'windows-1251'
            
            raw_text = response.text
            
            if raw_text.startswith('\r\n'):
                raw_text = raw_text[2:]
            
            match = re.search(r'"content":"(.+?)"', raw_text)
            if match:
                joke = match.group(1)
                joke = joke.replace('\\n', '\n').replace('\\r', '').replace('\\"', '"')
                return joke
            else:
                if '"content":"' in raw_text:
                    joke = raw_text.split('"content":"')[1].split('"')[0]
                    joke = joke.replace('\\n', '\n').replace('\\r', '').replace('\\"', '"')
                    return joke
                else:
                    return "Не удалось распарсить анекдот с сайта"
                
        except requests.exceptions.Timeout:
            logger.error("Таймаут при получении анекдота с rzhunemogu")
            return "Сайт с анекдотами временно недоступен. Попробуйте позже."
        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения с rzhunemogu")
            return "Нет соединения с сайтом анекдотов. Проверьте интернет."
        except Exception as e:
            logger.error(f"Ошибка при парсинге анекдота с rzhunemogu: {e}")
            return "Произошла ошибка при получении анекдота. Попробуйте еще раз."
    
    def get_gai_joke(self):
        return random.choice(self.gai_jokes) if self.gai_jokes else "Пока нет анекдотов про ГАИ"
    
    def get_moto_joke(self):
        return random.choice(self.moto_jokes) if self.moto_jokes else "Пока нет анекдотов про мотоциклы"
    
    def get_general_joke(self):
        return random.choice(self.general_jokes) if self.general_jokes else "Пока нет общих анекдотов"

joke_gen = JokeGenerator()

def is_admin(user_id):
    return user_id in ADMIN_IDS

def send_to_channel(joke, joke_type="анекдот"):
    try:
        bot.send_message(
            chat_id=CHANNEL_ID,
            message_thread_id=TOPIC_ID,
            text=f"😂 {joke_type}:\n\n{joke}"
        )
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки в канал: {e}")
        return False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = f"""
🤖 Привет! Я бот для анекдотов!

📋 Личные команды:
/anekdot - случайный анекдот
/anekdot_GAI - анекдот про ГАИ
/anekdot_MOTO - анекдот про мотоциклы
/random - случайный анекдот с сайта
/site_joke [тип] - анекдот с сайта по типу

📢 Команды для канала:
/send_gai - отправить анекдот про ГАИ в канал
/send_moto - отправить анекдот про мотоциклы в канал  
/send_general - отправить общий анекдот в канал
/send_random - отправить анекдот с сайта в канал
/send_mixed - случайный анекдот в канал

📊 Команды управления:
/reload_jokes - перезагрузить анекдоты
/joke_stats - статистика анекдотов

🌐 Типы анекдотов с сайта:
1-случайные, 2-Вовочка, 3-Штирлиц, 4-поручик Ржевский
5-Чебурашка, 6-детские, 11-семьи, 12-работа
13-алкоголь, 14-политика, 16-студенты, 18-армия
    """
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['anekdot'])
def send_anekdot(message):
    try:
        if random.choice([True, False]):
            joke = joke_gen.get_general_joke()
        else:
            joke = joke_gen.get_joke_from_rzhunemogu(1)
        bot.reply_to(message, f"😂 Анекдот:\n\n{joke}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка.")

@bot.message_handler(commands=['anekdot_GAI'])
def send_anekdot_gai(message):
    try:
        joke = joke_gen.get_gai_joke()
        bot.reply_to(message, f"🚓 Анекдот про ГАИ:\n\n{joke}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка.")

@bot.message_handler(commands=['anekdot_MOTO'])
def send_anekdot_moto(message):
    try:
        joke = joke_gen.get_moto_joke()
        bot.reply_to(message, f"🏍️ Анекдот про мотоциклы:\n\n{joke}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка.")

@bot.message_handler(commands=['random'])
def send_random(message):
    try:
        ctype = random.choice([1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 16, 18])
        joke = joke_gen.get_joke_from_rzhunemogu(ctype)
        bot.reply_to(message, f"🎲 Случайный анекдот:\n\n{joke}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка.")

@bot.message_handler(commands=['site_joke'])
def send_site_joke(message):
    try:
        parts = message.text.split()
        if len(parts) > 1:
            try:
                ctype = int(parts[1])
                valid_types = [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 16, 18]
                if ctype not in valid_types:
                    ctype = 1
            except ValueError:
                ctype = 1
        else:
            ctype = 1
        
        type_names = {
            1: "случайные", 2: "про Вовочку", 3: "про Штирлица",
            4: "про поручика Ржевского", 5: "про Чебурашку", 6: "детские",
            11: "про семьи", 12: "про работу", 13: "про алкоголь", 
            14: "про политику", 16: "про студентов", 18: "про армию"
        }
        
        type_name = type_names.get(ctype, "случайные")
        joke = joke_gen.get_joke_from_rzhunemogu(ctype)
        bot.reply_to(message, f"🌐 Анекдот ({type_name}):\n\n{joke}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "Ошибка. Формат: /site_joke [тип]")

@bot.message_handler(commands=['send_gai'])
def send_gai_to_channel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Только для администраторов!")
        return
    try:
        joke = joke_gen.get_gai_joke()
        if send_to_channel(joke, "Анекдот про ГАИ 🚓"):
            bot.reply_to(message, "✅ Отправлен в канал!")
        else:
            bot.reply_to(message, "❌ Ошибка отправки")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['send_moto'])
def send_moto_to_channel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Только для администраторов!")
        return
    try:
        joke = joke_gen.get_moto_joke()
        if send_to_channel(joke, "Анекдот про мотоциклы 🏍️"):
            bot.reply_to(message, "✅ Отправлен в канал!")
        else:
            bot.reply_to(message, "❌ Ошибка отправки")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['send_general'])
def send_general_to_channel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Только для администраторов!")
        return
    try:
        joke = joke_gen.get_general_joke()
        if send_to_channel(joke, "Анекдот 😂"):
            bot.reply_to(message, "✅ Отправлен в канал!")
        else:
            bot.reply_to(message, "❌ Ошибка отправки")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['send_random'])
def send_random_to_channel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Только для администраторов!")
        return
    try:
        ctype = random.choice([1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 16, 18])
        joke = joke_gen.get_joke_from_rzhunemogu(ctype)
        if send_to_channel(joke, "Случайный анекдот 🎲"):
            bot.reply_to(message, "✅ Отправлен в канал!")
        else:
            bot.reply_to(message, "❌ Ошибка отправки")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['send_mixed'])
def send_mixed_to_channel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Только для администраторов!")
        return
    try:
        choice = random.choice(['gai', 'moto', 'general', 'random'])
        if choice == 'gai':
            joke = joke_gen.get_gai_joke()
            joke_type = "Анекдот про ГАИ 🚓"
        elif choice == 'moto':
            joke = joke_gen.get_moto_joke()
            joke_type = "Анекдот про мотоциклы 🏍️"
        elif choice == 'general':
            joke = joke_gen.get_general_joke()
            joke_type = "Анекдот 😂"
        else:
            ctype = random.choice([1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 16, 18])
            joke = joke_gen.get_joke_from_rzhunemogu(ctype)
            joke_type = "Случайный анекдот 🎲"
        
        if send_to_channel(joke, joke_type):
            bot.reply_to(message, f"✅ Отправлен в канал!")
        else:
            bot.reply_to(message, "❌ Ошибка отправки")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['reload_jokes'])
def reload_jokes(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Только для администраторов!")
        return
    try:
        joke_gen.reload_jokes()
        bot.reply_to(message, "✅ Анекдоты перезагружены!")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['joke_stats'])
def joke_stats(message):
    stats_text = f"""
📊 Статистика анекдотов:

🚓 ГАИ: {len(joke_gen.gai_jokes)}
🏍️ МОТО: {len(joke_gen.moto_jokes)}  
😂 ОБЩИЕ: {len(joke_gen.general_jokes)}
📁 Всего: {len(joke_gen.gai_jokes) + len(joke_gen.moto_jokes) + len(joke_gen.general_jokes)}

📍 Канал: {CHANNEL_ID}
📂 Раздел ID: {TOPIC_ID}
    """
    bot.reply_to(message, stats_text)

if __name__ == "__main__":
    logger.info("Запускаем бота...")
    try:
        bot_info = bot.get_me()
        logger.info(f"Бот @{bot_info.username} запущен!")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
