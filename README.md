<img width="544" height="682" alt="image" src="https://github.com/user-attachments/assets/2c7b84b8-fd91-4ca9-80f9-64c06ba8ce14" />


🚀 Полная инструкция по установке бота с нуля

1. Подготовка сервера
# Подключитесь к серверу
ssh root@your_server_ip

# Обновите систему
apt update && apt upgrade -y

# Установите необходимые пакеты
apt install python3 python3-pip python3-venv git -y

2.Создание папки и настройка окружения

# Создайте папку для бота
mkdir /root/bot
cd /root/bot

# Создайте виртуальное окружение
python3 -m venv bot-env

# Активируйте виртуальное окружение
source bot-env/bin/activate

3. Установка зависимостей
   # Установите необходимые библиотеки
pip install pyTelegramBotAPI requests

# Или создайте файл requirements.txt
cat > requirements.txt << 'EOF'
pyTelegramBotAPI==4.14.1
requests==2.31.0
EOF

pip install -r requirements.txt

4. Создание файла бота
# Создайте основной файл бота
nano /root/bot/bot.py

Вставить, то что лежит гите

5. Создание файлов с анекдотами
   
# Создайте файлы
cd /root/bot
touch GAI.txt MOTO.txt GENERAL.txt

# Добавьте примеры анекдотов
echo "Останавливает гаишник машину: - Ваши права! - А за что?" >> GAI.txt
echo "Объявление: 'Продам мотоцикл. Не бит, не крашен.'" >> MOTO.txt
echo "Программист ставит чайник с водой на плиту..." >> GENERAL.txt

6. Настройка автозапуска через systemd

# Создайте systemd сервис
sudo nano /etc/systemd/system/telegram-joke-bot.service

Добавить: 

[Unit]
Description=Telegram Joke Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot
Environment=PATH=/root/bot/bot-env/bin
ExecStart=/root/bot/bot-env/bin/python /root/bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

7. Запуск и активация
   
# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable telegram-joke-bot.service

# Запустите бота
sudo systemctl start telegram-joke-bot.service

# Проверьте статус
sudo systemctl status telegram-joke-bot.service

# Посмотрите логи
sudo journalctl -u telegram-joke-bot.service -f

8. Проверка работы
   # Проверьте что бот запущен
ps aux | grep bot.py

# Проверьте логи
sudo journalctl -u telegram-joke-bot.service -n 10

9. Полезные команды для управления

    # Остановить бота
sudo systemctl stop telegram-joke-bot.service

# Перезапустить бота
sudo systemctl restart telegram-joke-bot.service

# Посмотреть статус
sudo systemctl status telegram-joke-bot.service

# Посмотреть логи
sudo journalctl -u telegram-joke-bot.service -n 20
