#Стороние модули
import random

import telebot
from telebot import apihelper
from telebot import types

import sqlite3

import re

import time as tm

import _thread


# Файлы
import config


def main():
    #sqlite
    db = sqlite3.connect('bot.db')
    sql = db.cursor()
    db.commit()
    
    
    #Надстройки 
    apihelper.proxy = {'http':'http://109.167.49.27'}
    bot = telebot.TeleBot(config.telegram_token)

    sol = 'j1a9z7z9'

    def welcome_keyboard(message):
        pass


        

    

    welcome_stickers = ['AAMCAgADGQEAAzZewWwwHuz2YaH-Is17VmfvzkVljQACWT0AAulVBRijqzo0B6P5FAtoN5IuAAMBAAdtAAPXBQACGQQ', 
                        'AAMCAgADGQEAAzZewWwwHuz2YaH-Is17VmfvzkVljQACWT0AAulVBRijqzo0B6P5FAtoN5IuAAMBAAdtAAPXBQACGQQ',
                        'AAMCAgADGQEAAzZewWwwHuz2YaH-Is17VmfvzkVljQACWT0AAulVBRijqzo0B6P5FAtoN5IuAAMBAAdtAAPXBQACGQQ',
                        'AAMCAgADGQEAAzZewWwwHuz2YaH-Is17VmfvzkVljQACWT0AAulVBRijqzo0B6P5FAtoN5IuAAMBAAdtAAPXBQACGQQ'
                        ]

    @bot.message_handler(content_types=['sticker'])
    #Получение стикера
    def get_sticker(message):
        print(message.sticker)
        
    #Cлучайный стикер
    def random_welcome():
        ran = (random.randrange(0, len(welcome_stickers)-1, 1))
        return(ran)

   
    
    
    
    #Приветствие
    @bot.message_handler(commands=['start'])
    def welcome(message):
        check = False
        check01 = False
        db = sqlite3.connect('bot.db')
        sql = db.cursor()
        bot.send_message(message.chat.id, 'Привет')
        sql.execute("SELECT chat FROM users WHERE chat = {0}".format(message.chat.id))
        select = sql.fetchone()
        print(select)
        if select == None:
            sql.execute('INSERT INTO users (chat) VALUES ({0})'.format(message.chat.id))
            db.commit()






    
    @bot.message_handler(content_types=['text'], regexp = r'./.')
    def note(message):
        def thread_note(message):
            db = sqlite3.connect('bot.db')
            sql = db.cursor()
            note_text = ''
            note_time = ''
            error = 0
            check = False
            for i in message.text:
                if i == '/':
                    error = error + 1
                    check = True
                elif check:
                    note_time = note_time + i
                    print(note_time)
                else:
                    note_text = note_text + i
            if error > 1:
                bot.send_message(message.chat.id, 'Похоже вы ввели неправильные символы')
            time = 0
            for i in note_time:
                if i == 's':
                    note_time = time
                    break
                elif i == 'm':
                    note_time = time * 60
                    break
                else:
                    time += int(i)







            print('Note Time: ' + str(note_time) + ' ' + '({0})'.format(message.chat.id))
            print('Note Text: ' + note_text + ' ' + '({0})'.format(message.chat.id))
            sql.execute('''INSERT INTO notes (time, chat, text)
                                    VALUES (?, ?, ?)''', (note_time, message.chat.id, note_text))

            db.commit()



            sql.execute("""SELECT id FROM notes 
                                WHERE time = ? AND  chat = ? AND  text = ?""", (note_time, message.chat.id, note_text))
            id = sql.fetchone()

            sql.execute("SELECT time FROM notes WHERE id = ?", (id))

            time = sql.fetchone()
            time = str(time)
            time = re.sub(r"[(),]", "", time)
            time = int(time)
            tm.sleep(time)
            sql.execute("SELECT text FROM notes WHERE id = ?", (id))
            bot.send_message(message.chat.id, sql.fetchone())
        _thread.start_new_thread(thread_note, (message, ))



    bot.polling(none_stop=True)
    


if __name__ == "__main__":
    main()