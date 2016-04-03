
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
      print (list_name)

def remove_user_list(file, list_name, person):
    'Removes the user from the memory and saves it into a file.'
    try:
        list_name.remove(person)
        save_list(file, list_name)
        #After successful process sends "user is unblocked!" message to the admin
        bot.send_message(config.my_id,"User is unblocked!")
        print (list_name)
    except ValueError:
        #If the user id is not present in the list it prompts with "Oops! User is not blocked."
        bot.send_message(config.my_id,"Oops! User is not blocked.")
        print (list_name)
        return


