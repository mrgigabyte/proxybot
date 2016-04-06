#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import config
import dbhelper
import dictionary
import os

# Initialize bot
bot = telebot.TeleBot(config.token)

#checks whether the file is having some presaved data or not
#if the file contains no data then ---> makes a list with the name user_list with just []
#else it loads the previous list and stores it in the var user_list
if os.stat(config.storage_block).st_size == 0:
   user_list = list()
else:
   user_list = dictionary.load_list(config.storage_block)

# Handle always first "/start" message when new chat with your bot is created
@bot.message_handler(func=lambda message: message.chat.id != config.my_id, commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Hey Buddy! Write me your text and the admin will get in touch with you shortly.")

# Handle the messages which are not sent by the admin user(the one who is handling the bot) sends texts, audios, document etc to the admin
@bot.message_handler(func=lambda message: message.chat.id != config.my_id, content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video',
                                    'voice', 'location', 'contact'])
#checks whether we have blocked that user via bot or not
def blockk(message):
   z = "'"+ str(message.chat.id) + "'"
#checks whether the message.chat.id of the user is there in the block list (user_list)
#if message.chat.id present ---> sends a message to the user that he/she is blocked
#else forwards the message to the admin
   if str(message.chat.id) in user_list:
      bot.send_message(message.chat.id, "Woops your ass is blocked!")
   else:
    bot.forward_message(config.my_id, message.chat.id,    message.message_id)
    dbhelper.add_message(message.message_id + 1, message.chat.id)
    bot.send_message(config.my_id,'\n /block' + str(message.chat.id) + '\n/unblock' + str(message.chat.id))
    #sends /block and /unblock command to the admin concated with theh message.chat.id of the user

@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["text"])
def my_text(message):
    
    # If we're just sending messages to bot (not replying) -> do nothing and notify about it.
    # Else -> get ID whom to reply and send message FROM bot.
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        bot.send_chat_action(who_to_send_id, action = 'typing')
        #shows the user that the bot is typing at the moment
        if who_to_send_id:
            # You can add parse_mode="Markdown" or parse_mode="HTML", however, in this case you MUST make sure,
            # that your markup if well-formed as described here: https://core.telegram.org/bots/api#formatting-options
            # Otherwise, your message won't be sent.
            bot.send_message(who_to_send_id, message.text)
            # Temporarly disabled freeing message ids. They don't waste too much space
            # dbhelper.delete_message(message.reply_to_message.message_id)
    else:      
       #checks whether the admin has entered /block or /unblock command
       #if /block --> true then it gives the message.chat.id number as STRING after first 6 characters
       #else it checks for /unblock and returns message.chat.id number as STRING after first 8 characters
       #if none of the above evaluates to true then it sends "no one to reply"
       if '/block'in message.text:      
             #if /block is true then it saves message.chat.id of the user as string in the user_list of the desired file
             dictionary.add_new_user(config.storage_block, user_list, message.text[6:])
       elif '/unblock' in message.text:
             #if /unblock is true then it removes message.chat.id of the particular user from the user_list of the desired file
             dictionary.remove_user_list(config.storage_block, user_list, message.text[8:])             
       else:
          bot.send_message(message.chat.id, "No one to reply!")
            
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["sticker"])
def my_sticker(message):
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id    (message.reply_to_message.message_id)
         
        if who_to_send_id:
            bot.send_sticker(who_to_send_id, message.sticker.file_id)
            bot.send_chat_action(who_to_send_id, action = 'typing')
    else:
        bot.send_message(message.chat.id, "No one to reply!")


@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["photo"])
def my_photo(message):
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        bot.send_chat_action(who_to_send_id, action = 'upload_photo')
        if who_to_send_id:
            # Send the largest available (last item in photos array)
            bot.send_photo(who_to_send_id, list(message.photo)[-1].file_id)
    else:
        bot.send_message(message.chat.id, "No one to reply!")


@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["voice"])
def my_voice(message):
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "record_audio")
            bot.send_voice(who_to_send_id, message.voice.file_id, duration=message.voice.duration)
    else:
        bot.send_message(message.chat.id, "No one to reply!")


@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["document"])
def my_document(message):
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        bot.send_chat_action(who_to_send_id, action = 'upload_document')
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "upload_document")
            bot.send_document(who_to_send_id, data=message.document.file_id)
    else:
        bot.send_message(message.chat.id, "No one to reply!")


@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["audio"])
def my_audio(message):
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        bot.send_chat_action(who_to_send_id, action = 'upload_audio')
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "upload_audio")
            bot.send_audio(who_to_send_id, performer=message.audio.performer,
                           audio=message.audio.file_id, title=message.audio.title,
                           duration=message.audio.duration)
    else:
        bot.send_message(message.chat.id, "No one to reply!")


@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["video"])
def my_video(message):
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        bot.send_chat_action(who_to_send_id, action = 'upload_video')
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "upload_video")
            bot.send_video(who_to_send_id, data=message.video.file_id, duration=message.video.duration)
    else:
        bot.send_message(message.chat.id, "No one to reply!")


# No Google Maps on my phone, so this function is untested, should work fine though.
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["location"])
def my_location(message):
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        bot.send_chat_action(who_to_send_id, action = 'find_location')
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "find_location")
            bot.send_location(who_to_send_id, latitude=message.location.latitude, longitude=message.location.longitude)
    else:
        bot.send_message(message.chat.id, "No one to reply!")


if __name__ == '__main__':
    bot.polling(none_stop=True)
