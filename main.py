import telebot
from config import *
from newsapi import NewsApiClient
from telebot import types

newsapi = NewsApiClient(api_key='4dd59dab99dd4eadbec05f5b77c34cac')

bot = telebot.TeleBot("6522103895:AAH8N5gh6YfGbZnKdp6BWuaBl8vIAx9wDSM")
from telebot import types

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id=[message.chat.id]
    connect = sqlite3.connect("bd.db")
    cursor = connect.cursor()
    user = cursor.execute("SELECT * from users where tg_id = ?;",(user_id)).fetchone()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_news = types.KeyboardButton('Новости')
    button_categories = types.KeyboardButton('Категории')
    button_sub = types.KeyboardButton('Подписки')
    markup.add(button_news,button_categories,button_sub)
    if not user:
        cursor.execute("insert into users ('tg_id') values (?);", user_id)
        connect.commit()
        bot.reply_to(message, "Вы успешно зарегистрировались",reply_markup=markup)
    else:
        bot.reply_to(message, "Вы уже зарегистрированы",reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    connect = sqlite3.connect("bd.db")
    cursor = connect.cursor()
    if message.chat.type=='private':
        if message.text=='Категории':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            categories=cursor.execute('''SELECT * FROM categories''').fetchall()
            i=0
            while i <len(categories):
                categor = types.KeyboardButton('+ ' + categories[i][1])
                i=i+1
                markup.add(categor)
            bot.reply_to(message,'Категории',reply_markup=markup)


    if message.chat.type == 'private':
        pattern = '+'
        if message.text.startswith(pattern):
            user_id = [message.chat.id]
            print("user_id")
            id=cursor.execute('''SELECT id FROM users WHERE tg_id = ?''', (user_id)).fetchone()
            id=str(id[0])

            subs =cursor.execute('''SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.id_category WHERE id_user = ? ;''', (id)).fetchall()

            mass = []
            i = 0
            while i < len(subs):
                mass.append(subs[i][3])
                i=i+1
            i = 0
            count = 0
            name_sub = message.text[2:]
            while i < len(mass):
                if name_sub == mass[i]:
                    count = count + 1
                i = i + 1
            if count == 0:
                cat_id = cursor.execute('''SELECT id FROM categories WHERE name = ? ; ''', (name_sub,)).fetchall()
                cursor.execute('''INSERT INTO subscribes ('id_user', 'id_category') VALUES (?, ?) ''',(id,cat_id[0][0]))
                connect.commit()
                bot.reply_to(message, 'Вы подписаны')
            else:
                bot.reply_to(message, 'Вы уже подписаны')
                connect = sqlite3.connect("bd.db")
                cursor = connect.cursor()


    if message.chat.type == 'private':
        if message.text == 'Подписки':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            subscribes = cursor.execute('''SELECT name FROM categories INNER JOIN subscribes ON categories.id=subscribes.id_category''').fetchall()
            i = 0
            while i < len(subscribes):
                print(subscribes[i])
                sub = types.KeyboardButton('- ' + subscribes[i][0])
                i = i + 1
                markup.add(sub)
            bot.reply_to(message, 'Подписки', reply_markup=markup)


    if message.chat.type == 'private':
        if message.text == 'Новости':
            userid = [message.chat.id]
            connect = sqlite3.connect('bd.db')
            cursor = connect.cursor()

            id = cursor.execute('SELECT id FROM users WHERE tg_id=?;', (userid)).fetchone()
            id = str(id[0])
            sub = cursor.execute(
                'SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.id_category WHERE id_user = ?;',
                (id,)).fetchall()

            i = 0

            while i < len(sub):

                top_headlines = newsapi.get_top_headlines(category=f'{sub[i][3]}', language='ru', country='ru',
                                                                  page=1, page_size=1)
                bot.send_message(message.chat.id,
                        f'Категория:{sub[i][3]}\nЗаголовок: {top_headlines["articles"][0]["title"]}\n {top_headlines["articles"][0]["url"]}')
            
        if message.chat.type == 'private':
            pattern = '-'
        if message.text.startswith(pattern):
            user_id = [message.chat.id]
            id = cursor.execute('''SELECT id FROM users WHERE tg_id = ?''', (user_id)).fetchone()
            id = str(id[0])

            subs = cursor.execute(
                '''SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.id_category WHERE id_user = ? ;''',
                (id)).fetchall()
            mass = []
            i = 0

            count = 0
            name_sub = message.text[2:]
            # print(name_sub)
            while i < len(mass):
                if name_sub == mass[i]:
                    # print(mass[i])
                    count = count + 1
                i = i + 1
            cat_id = cursor.execute('''SELECT id FROM categories WHERE name = ? ; ''', (name_sub,)).fetchall()
            cursor.execute('''DELETE FROM subscribes 
               WHERE id_user = ? AND id_category = ?''',
                           (id, cat_id[0][0]))
            connect.commit()
            bot.reply_to(message, 'Вы отписались')

bot.infinity_polling(none_stop=True)

