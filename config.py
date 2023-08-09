import configparser

config = configparser.ConfigParser()# объект конфига


config.add_section('Secret_data')# секция
config.set('Secret_data', 'API_key_bot', 'BOT_TOKEN')# параметр1 токен бота
config.set('Secret_data', 'API_key_fix', 'TOKEN_fixer.io')# параметр2 токен fixer io

# Записываем конфигурацию в файл
with open('config.ini', 'w') as f:
    config.write(f)