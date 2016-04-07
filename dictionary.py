
#Python file for maintaining the overall users
#and
#Python File for maintaining the blocked users

import telebot
import config
import dbhelper

bot = telebot.TeleBot(config.token)


def create_list(file,list_name=None):
    'Returns a new created file as list.'
    if list_name == None:
       list_name = list()       
       with open(file, 'a') as f:
          f.write(str(list_name))
       print(file, 'created!')    
       return list_name

def load_list(file):
    'Returns a loaded file as a list.'
    temp_list = list()
    try:
        with open(file, 'r', encoding='utf8') as f:
            temp_list = eval(f.read())
        return temp_list
    
    except FileNotFoundError:
        return create_list(file)

def save_list(file, list_name):
    'Saves a list into a file.'  
    try:
        with open(file, 'w', encoding='utf8') as f:
            f.write(str(list_name))
            
    except FileNotFoundError:
        create_list(file, list_name)

def add_new_user(file, list_name, person):
    'Adds a new user to the memory and saves it into a file.'
    if person not in list_name:
      list_name.append(person)
      save_list(file, list_name)
      #After successful process sends "user is blocked" message to the admin
      bot.send_message(config.my_id,"User is blocked!")       
    else:
      #If the user id already exists in the list it prompts with "User is blocked already!"
      bot.send_message(config.my_id,"User is blocked already!")
      
def remove_user_list(file, list_name, person):
    'Removes the user from the memory and saves it into a file.'
    try:
        list_name.remove(person)
        save_list(file, list_name)
        #After successful process sends "user is unblocked!" message to the admin
        bot.send_message(config.my_id,"User is unblocked!")
        
    except ValueError:
        #If the user id is not present in the list it prompts with "Oops! User is not blocked."
        bot.send_message(config.my_id,"Oops! User is not blocked.")
        return

def create_dict(file, dict_name=None):
    'Returns a new created file as dictionary.'
    if dict_name == None:
        dict_name = dict()
        
    with open(file, 'a') as f:
        f.write(str(dict_name))
    print(file, 'created!')
    
    return dict_name

def load_dict(file):
    'Returns a loaded file as a dictionary.'
    temp_dict = dict()
    try:
        with open(file, 'r', encoding='utf8') as f:
            temp_dict = eval(f.read())
        return temp_dict
    
    except FileNotFoundError:
        return create_dict(file)

def save_dict(file, dict_name):
    'Saves a dictionary into a file.'  
    try:
        with open(file, 'w', encoding='utf8') as f:
            f.write(str(dict_name))
            
    except FileNotFoundError:
        create_dict(file, dict_name)

def add_key_dict(file, dict_name, key, val):
    'Adds a key and a value to the memory and saves it into a file.'
    dict_name[key] = val
    save_dict(file, dict_name)

def remove_key_dict(file, dict_name, key):
    'Removes a key from the memory and saves it into a file.'
    try:
        del dict_name[key]
        save_dict(file, dict_name)
        
    except KeyError:
        print('Key:', key, 'not found!')
        return

#adds the username/nickname of the user in the block list
def add_blocklist(file, person):
    user = [line.rstrip('\n') for line in open(file,'rt')]
    if str(person).lower() not in user:
        user.append(str(person).lower())
        with open(file, 'a') as f:
            f.write(str(person).lower()+"\n")    

#rempves the username/nickname of the user from the block list
def remove_from_blocklist(file, person):
    f = open(file,"r")
    lines = f.readlines()
    f.close()
    f = open(file,"w")
    for line in lines:
        if line!=person.lower()+"\n":
              f.write(line)
    f.close()

#step handler for adding the nickname as the key for the dictionary
def process_name_step(message, dict_name=None, file=None, val=None ):
    try:
      if dict_name !=None and file != None and val !=None:
          key = message.text
          lower_key = key.lower()
          else:
          add_key_dict(file, dict_name, lower_key, val)
          bot.reply_to(message,"Thanks! " +"\n"+ "*Remember to block this user with the name:* "+"`'"+key+"'`"+" *only!*",parse_mode="Markdown" )
    except Exception as e:
      bot.reply_to(config.my_id, 'oooops')

#for setting the status of the admin 
def set_status(file, status):
    with open(file,"w") as text_file:
      text_file.write(str(status).lower())

#for checking the status of the admin
def check_status(file):
    with open(config.storage_availability) as f:
      z = f.read()
      if z == "unavailable":
       return "false"
       print (z)
      else:
       return "true"
       print (z)

#for adding the message.chat.id's of the user in the file
def add_avaiblist(file, person):
    user = [line.rstrip('\n') for line in open(file,'rt')]
    if str(person) not in user:
        user.append(str(person))
        with open(file, 'a') as f:
            f.write(str(person)+"\n")  

#for setting the unavailable message for the admin
def unvb_msg(message, file=None):
    try:
      if file != None:
          unvbmsg = message.text
          with open(file,"w") as msg_file:
             msg_file.write(str(unvbmsg))
          bot.reply_to(message,"Thanks! " +"\n"+ "*The Message has been set successfully* ",parse_mode="Markdown" )
    except Exception as e:
      bot.reply_to(config.my_id, 'oooops! something went wrong')


