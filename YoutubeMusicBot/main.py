import json
import os
import shutil
from datetime import datetime
from os.path import isfile
import telebot
from pytube import YouTube

token = ''
bot = telebot.TeleBot(token)
jsonfilename = 'logs.json'


def createFiles():
    data = {
        "chats": {},
        "logs": [],
        "users": {}
    }
    with open(jsonfilename, "w") as file:
        json.dump(data, file, indent=4)
    file.close()


def appendChats(chat_id):
    if not isfile(jsonfilename):
        createFiles()
    with open(jsonfilename, "r+") as file:
        data = json.load(file)
        if chat_id in data['chats']:
            file.close()
            return
        data['chats'][str(chat_id)] = None
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()


def appendLogs(new_data, txt):
    if not isfile(jsonfilename):
        createFiles()
    file = open('logs.txt', 'a+')
    file.write(txt)
    with open(jsonfilename, "r+") as file:
        data = json.load(file)
        data['logs'].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()


def appendUsers(new_data, user_id):
    if not isfile(jsonfilename):
        createFiles()
    with open(jsonfilename, "r+") as file:
        data = json.load(file)
        try:
            data['users'][str(user_id)]
        except:
            data['users'][str(user_id)] = []
        finally:
            data['users'][str(user_id)].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()


def writeFiles(message):
    message = message.json
    message_id = message['message_id']
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    username = message['from']['username']
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    firstname = message['from']['first_name']
    text = message['text']
    data_logs = {
        'message_id': message_id,
        'chat_id': chat_id,
        'user_id': user_id,
        'username': username,
        'first_name': firstname,
        'date_time': now,
        'url': text
    }
    data_json = {
        'message_id': message_id,
        'chat_id': chat_id,
        'date_time': now,
        'url': text
        }
    data_txt = f'{message_id} {chat_id} {user_id} {username} {firstname} {now} {text}\n'
    appendLogs(data_logs, data_txt)
    appendUsers(data_json, user_id)


def deleteDir(chat_id):
    try:
        script_dir = os.path.abspath(os.path.dirname(__file__))
        shutil.rmtree(f'{script_dir}/files/{chat_id}')
    finally:
        print(f'Directory of {chat_id} has been deleted!')


def downloadFile(message):
    yt = YouTube(message.text)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=f'files/{message.chat.id}/')
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded.")
    return new_file


@bot.message_handler(commands=['start', 'help'])
def start(message):
    mess = f'Video duration should be less than 2 hours. Long videos may take some time to be uploaded. Just type the '\
           f'URL of the video You want to download :) '
    bot.send_message(message.chat.id, mess, parse_mode='html')
    appendChats(message.chat.id)


@bot.message_handler()
def sendMusic(message):
    try:
        audio = open(downloadFile(message), 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
        writeFiles(message)
        deleteDir(message.chat.id)
        bot.delete_message(message.chat.id, message.message_id)
    except:
        bot.send_message(message.chat.id, 'Wrong URL :(', parse_mode='html')


bot.polling(none_stop=True)
