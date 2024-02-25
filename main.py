import telebot
from telebot import types
import webbrowser
import requests
from bs4 import BeautifulSoup as BS
from decouple import config

bot = telebot.TeleBot(config('TOKEN'))


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'Wow, looks so cool!')


@bot.message_handler(commands=['start', 'main'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('My inst', url='https://www.instagram.com/noahrrly')
    markup.row(btn1)

    bot.send_message(message.chat.id, f'<b>Hello, {message.from_user.first_name}\n\nWhat i can do? Well...\n\n - I can open You Tube:  just write smth with this name\n\n- I can google:  Write what you want to know about in the form: "tell about ..." and I will google it</b>', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help information</b>', parse_mode='html')

@bot.message_handler()
def info(message):


    if 'hello' in message.text.lower():
        bot.send_message(message.chat.id, f'Oh, hello {message.from_user.first_name}!')

    if message.text.lower() == 'id':
        bot.reply_to(message, f'id: {message.from_user.id}')

    if len(message.text) < 10:
        if ('youtube' in message.text.lower()) or ('yt' in message.text.lower()) or ('you tube' in message.text.lower()):
            webbrowser.open('https://www.youtube.com')

    if 'tell about' in message.text.lower():

        if len(message.text) >= 11:

            usertxt = message.text.replace('tell about ', '')
            usertxt = usertxt.replace(' ', '_')
            print(usertxt)
            res = ''
            r = requests.get('https://en.wikipedia.org/wiki/' + usertxt)

            html = BS(r.content, 'html.parser')

            for el in html.select('.mw-page-container-inner > .mw-content-container'):
                for i in el.select('.mw-body-content > .mw-parser-output'):
                    for j in i.select('.mw-parser-output > p'):
                        res += j.text

            newres = ''

            while len(newres) < 200:
                for i in res.split('\n'):
                    if i == '':
                        continue
                    elif i != '':
                        if len(newres + i) < 1000:
                            newres += i
            for i in newres:
                if newres.count('[') > 0:
                    firstind = newres.index('[')
                    secondind = newres.index(']')
                    newres = newres[:firstind:] + ' ' + newres[secondind + 1::]

            bot.send_message(message.chat.id, newres)

bot.polling(none_stop = True)