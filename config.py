# -*- coding: utf-8 -*-

# Bot's token. Obtain yours from https://telegram.me/botfather
token = "TOKEN"


storage_name = "StorageUser"
storage_block = 'txtfiles/chatids.txt'
storage_userdir = 'txtfiles/userdir.txt'
storage_blocklist = 'txtfiles/blocklist.txt'
storage_availability = 'txtfiles/availability.txt'
storage_avaiblist = 'txtfiles/avaiblist.txt'
storage_nonavailmsg = 'txtfiles/nonavailmsg.txt'
storage_namelist = 'txtfiles/namelist.txt'
storage_fnamelist = 'txtfiles/fnamelist.txt'
# Your own chat id. Ask https://telegram.me/my_id_bot to tell you yours
my_id = yourid

'''
Here are things you should know:
storage_name        : storing all the message.id and chat.id of users. Format: database
storage_block       : storing all the chat ids of the blocked users in the form of a list
storage_userdir     : stores all the users who have sent a message (can be text, voice note etc etc). Stores in the form of dictionary
                      key: username val: message.chat.id  if username is not there then it will ask you for a 'nick name' as key
storage_blocklist   : stores all the usernames for the ones who are blocked. Admin can send /viewblocklist command to see the whole blocklist
storage_availability: stores whether admin status is "available" or "unavailable"
storage_avaiblist   : stores all the message.chat.id's of the user. Almost similar to userdir except that this is not a dictionary 
                      and doesn't store username
storage_nonavailmsg : stores the message that the user will get once the admin's status has been set to unavailable
storage_namelist    : stores the nick-names of the users in the form of dictionary key: Nick-name val: First-Name

PS: there's a blank.txt under the dir textfiles PLEASE DON'T delete that, it is used in proxy_bot.py.
I would recommend you to NOT to change the names of the text files but it's up to you.

'''
