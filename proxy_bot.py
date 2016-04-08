#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import config
import dbhelper
import dictionary
import fnmatch
import os

# Initialize bot
bot = telebot.TeleBot(config.token)

#checks whether the file is having some pre-saved data or not
#if the file contains no data then ---> makes a list/dict with the name user_list with just [] and user_dir with just a blank dict
#else it loads the previous list/dict and stores it in the var user_list for the list and var user_dir for the dict()
if os.stat(config.storage_block).st_size == 0:
   user_list = list()
else:
   user_list = dictionary.load_list(config.storage_block)

if os.stat(config.storage_userdir).st_size == 0:
   user_dir = dict()
else:
   user_dir = dictionary.load_dict(config.storage_userdir)

#for the list of all the commands
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["help"])
def command_start(message):
    bot.send_message(message.chat.id, """*Hey """ + message.chat.first_name +"""!\nSo, here is a list of commands that you should keep in mind:* \n 
`1`- /available  : sets your current status as available
`2`- /unavailable: sets your current status as unavailable 
`3`- /viewunavailablemessage : to view your Unavailable Message
`4`- /setunavailablemessage  : set the text message that you want users to see when you're unavailable 
`5`- /checkstatus: allows your to check your current status
`6`- /block `@username/nickname`  : allows you to block a user
`7`- /unblock `@username/nickname`: allows you to unblock a blocked user
`8`- /viewblockmessage: to view the block message (that the users will see)
`9`- /setblockmessage : set the text message that you want users to see when they are blocked
`10`-/viewblocklist  : allows you to view the list of blocked users
`11`-/viewnicknames  : allows you to view all the nicknames (with Firstname as reference)\n
*For any help and queries please contact -* [me](telegram.me/mrgigabytebot) *or check out* [this](https://github.com/mrgigabyte/proxybot)""",parse_mode="Markdown")


#command for admin: Used to view the block message
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["viewblockmessage"])
def command_start(message):
       with open(config.storage_blockmsg) as f:
          if os.stat(config.storage_nonavailmsg).st_size == 0:
            bot.send_message(message.chat.id, """*Oops!*
You haven't set any *Block Message* for the users. 
To set one kindly send: /setblockmessage to me""",parse_mode="Markdown")
          else:
            bot.send_message(message.chat.id,"`Your Block Message:`"+"\n"+ f.read(), parse_mode="Markdown")

#command for admin to set the block message that the user after getting blocked
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["setblockmessage"])
def command_start(message):
    blockmsg = bot.send_message(message.chat.id, "Alright now send me your text that you want the user to see when he/she is *blocked*",parse_mode="Markdown")
    bot.register_next_step_handler(blockmsg, lambda m: dictionary.unvb_msg(m, file=config.storage_blockmsg))

#to view all the nicknames in the format --> nick-name : user first name
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["viewnicknames"])
def command_nicknamelist(message):
    with open(config.storage_fnamelist) as f:
       if os.stat(config.storage_fnamelist).st_size == 0:
          bot.send_message(message.chat.id, "No nicknames yet!")
       else:
          bot.send_message(message.chat.id,"`Nick Names:`" +"\n"+ "`(nick name: first name)`"+"\n"+ f.read(), parse_mode="Markdown")


#command for admin: Used to view the whole Block List containing usernames and nicknames of the blocked users, refer config.py for more info
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["viewblocklist"])
def command_blocklist(message):
    with open(config.storage_blocklist) as f:
       if os.stat(config.storage_blocklist).st_size == 0:
          bot.send_message(message.chat.id, "No user is blocked!")
       else:
          bot.send_message(message.chat.id,"`Block List:`"+"\n"+ f.read(), parse_mode="Markdown")

#command for admin: Used to view your Unavailable Message
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["viewunavailablemessage"])
def command_start(message):
       with open(config.storage_nonavailmsg) as f:
          if os.stat(config.storage_nonavailmsg).st_size == 0:
            bot.send_message(message.chat.id, """*Oops!*
You haven't set any Unavailable message for the users. 
To set one kindly send: /setunavailablemessage to me""",parse_mode="Markdown")
          else:
            bot.send_message(message.chat.id,"`Your Unavailable Message:`"+"\n"+ f.read(), parse_mode="Markdown")

# Handle always first "/start" message when new chat with your bot is created (for users other than admin)
@bot.message_handler(func=lambda message: message.chat.id != config.my_id, commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Hey "+ message.chat.first_name +"!"+"\n"+" Write me your text and the admin will get in touch with you shortly.")
    
#command for admin to set the message the users will see when the admin status is set to unavailable
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["setunavailablemessage"])
def command_start(message):
    unvb = bot.send_message(message.chat.id, "Alright now send me your text that you want others to see when you're *unavailable*",parse_mode="Markdown")
    bot.register_next_step_handler(unvb, lambda m: dictionary.unvb_msg(m, file=config.storage_nonavailmsg))

#command for admin to set his/her status as available, this will simply re-write the availability.txt file with the text "available"
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["available"])
def command_start(message):
    bot.send_message(message.chat.id, "Your Status has been set as *Available*",parse_mode="Markdown")
    dictionary.set_status(config.storage_availability,"Available")

#command for admin to set his/her status as unavailable, this will simply re-write the availability.txt file with the text "unavailable"
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["unavailable"])
def command_start(message):
    bot.send_message(message.chat.id, "Your Status has been set as *Unavailable*",parse_mode="Markdown")
    dictionary.set_status(config.storage_availability,"Unavailable")

#command for the admin to check his/her current status. The .checkstatus() method simply reads the text in the availability.txt file
@bot.message_handler(func=lambda message: message.chat.id == config.my_id, commands=["checkstatus"])
def command_start(message):
     ww = dictionary.check_status(config.storage_availability)
     if ww == "false":
        bot.send_message(message.chat.id, "Your current status  is *Unavailable*",parse_mode="Markdown")
     else:
        bot.send_message(message.chat.id, "Your current status  is *Available*",parse_mode="Markdown")
  
# Handle the messages which are not sent by the admin user(the one who is handling the bot) sends texts, audios, document etc to the admin
@bot.message_handler(func=lambda message: message.chat.id != config.my_id, content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video',
                                    'voice', 'location', 'contact'])
#checks whether the admin has blocked that user via bot or not
def blockk(message):
  if message.chat.id in user_list:
     with open(config.storage_blockmsg) as t:
        bot.send_message(message.chat.id, t.read())

  else:
   #forwards the message sent by the user to the admin. Only if the user is not blocked
   bot.forward_message(config.my_id, message.chat.id,    message.message_id)
   dbhelper.add_message(message.message_id + 1, message.chat.id)
   dictionary.add_avaiblist(config.storage_avaiblist,message.chat.id) #adds the message.chat.id of the user in avaiblist.txt check config.py
   q = dictionary.check_status(config.storage_availability) #checks the status of the admin whether he's available or not
   if q == "false": #if not available then the user gets the unavailable text message from unavailmsg.txt check config.py
      x = [line.rstrip('\n') for line in open(config.storage_avaiblist,'rt')]
   else: #if the admin is available then the bot functions normally as the way it should
      x = [line.rstrip('\n') for line in open('txtfiles/blank.txt','rt')]
   if str(message.chat.id) in x: 
      with open(config.storage_nonavailmsg) as m:
        bot.send_message(message.chat.id, m.read())
   """
   from here the code is about saving the data of all the users in the form of a dictionary with key : username and val: message.chat.id
   There can be many possibilities and chances of error, I've made sure to cover all of them but who knows o_0
   Okay! So here are the cases:
   1: user has a username and is a new user for the bot
   2: user doesnt have a username and is a new user for the bot
   3: user changed his username but is an old user for the bot
   4: user removed his username and is an old user for the bot
   5: idk that's it ? 
   
   if message.chat.id not in user_dir.values() <-- here the bot checks whether the message.chat.id of the user exists in the dict or not
   if not: <--meaning it's a new user
     then it checks for the username
       if user doesnt have a username then ---> it asks the admin to give a nickname for the user to save that as key
       else it saves the username of the new user as the key and chat.id as the val
       We've successfully covere the cases 1 & 2 ^
   Now if message.chat.id is presentt in user_dir.values() 
   if yes: <---meaning its an old user 
      it then checks whether the username is present or not 
           if the user doesnt has a username (meaning the old user removed his/her username)
           then it cross checks in the dict whether the key of the user has '@' or not
               now here's the tricky part: why did I check for '@' ? because in the case 2 we have given a nick name 
               to the user so now assume a case :
                     the new user opens the bot writes a text to the bot, the bot checks the chat.id of the user since it's not 
                     there and the user doesnt has a username it will ask the admin to give a nickname. 
                     NOW! if the user will write a text message again then since the chat.id of the user is now present in the 
                     dict() the user will be treated as an old user with the key as the nickname. So, the else part of the code 
                     will execute. Now! here we are only considering the old users and not the users who already have a nickname
                     and hence to differentiate among the two we have checked for '@' symbol in the key.
               Hence, if the user is old and doesnt have a username then it will ask the admin for the new nickname
               We have successfully covered the case 4 ^
            if the old user has a nickname then it checks whether the username is already present or not
                if not: then it saves the data of the user with the key as the new username and message.chat.id as the val
                if yes: then do nothing 
   Hence, we have covered all the possible cases
  
   """
   if message.chat.id not in user_dir.values():    
     if message.chat.username == None:
        msg = bot.send_message(config.my_id, "*Uh! the user does not have a username o_0*\nCan you please suggest a name that can be used to store the data of the following user ?\n *PS: The nickname should be unique and shouldn't contain* '`@`'",parse_mode="Markdown" )
        bot.register_next_step_handler(msg, lambda m: dictionary.process_name_step(m, dict_name=user_dir, file=config.storage_userdir, val=message.chat.id, firstname = message.chat.first_name))
           
     else:
        userName = "@"+ message.chat.username
        userName = userName.lower()
        #checks whether the message.chat.id of the user is there in the block list (user_list)
        #if message.chat.id present ---> sends a message to the user that he/she is blocked
        #else forwards the message to the admin
        if userName not in user_dir:   
            dictionary.add_key_dict(config.storage_userdir, user_dir, userName, message.chat.id)     
   else:
     if message.chat.username == None:
       for userName, chatid in user_dir.items():
          if chatid == message.chat.id:
              z = userName
              if '@' in z:
                  msg = bot.send_message(config.my_id, "*Uh! the user does not have a username o_0*\nCan you please suggest a name that can be used to store the data of the following user ?\n *PS: The nickname should be unique and shouldn't contain* '`@`'",parse_mode="Markdown" )
                  bot.register_next_step_handler(msg, lambda m: dictionary.process_name_step(m, dict_name=user_dir, file=config.storage_userdir, val=message.chat.id, firstname = message.chat.first_name))
     else:
        userName = "@"+ message.chat.username
        userName = userName.lower()
        if userName not in user_dir:   
            dictionary.add_key_dict(config.storage_userdir, user_dir, userName, message.chat.id) 


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
            #if /block is true then it gets the username of the user and adds his/her id from the block list
          if fnmatch.fnmatch(message.text,'/block *'):  #check whether the text message is /block 'random character' using the wildcard: *
             userid = message.text[6:].strip()
             chat_id = user_dir.get(userid.lower())
             #it can happen that the admin has entered wrong username/nickname and if that evaluates to be true then:
             if chat_id == None:
                bot.send_message(message.chat.id, """*Oops!*\nEither the user has never operated this bot or the username entered is incorrect
*Please try again :I*""",parse_mode="Markdown")
             else:
                dictionary.add_new_user(config.storage_block, user_list, chat_id)
                dictionary.add_blocklist(config.storage_blocklist, userid)
          elif message.text == '/block':
             bot.send_message(message.chat.id, """Woops! you did a mistake, please type the username of the user you want to block after the command
Like:
/block `@username/nickname`""",parse_mode="Markdown") 
       elif '/unblock' in message.text:
             #if /unblock is true then it gets the username of the user and removes his/her id from the block list
         if fnmatch.fnmatch(message.text,'/unblock *'):  #check whether the text message is /unblock 'random character' using the wildcard: *
             userid = message.text[8:].strip()
             chat_id = user_dir.get(userid.lower())
             if chat_id == None:
                bot.send_message(message.chat.id, """*Oops!*\nEither the user has never operated this bot or the username entered is incorrect
*Please try again :I*""",parse_mode="Markdown")
             else:
                dictionary.remove_user_list(config.storage_block, user_list, chat_id)     
                dictionary.remove_from_blocklist(config.storage_blocklist, userid)    
         elif message.text == '/unblock':
             bot.send_message(message.chat.id, """Woops! you did a mistake, please type the username of the user you want to unblock after the command
Like:
/unblock `@username/nickname`""",parse_mode="Markdown")    
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
