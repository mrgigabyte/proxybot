#<p align="center">Telegram Proxy Bot 
<p align="center">A simple BITM, for [Telegram](https://telegram.org/) acting as some kind of "proxy". Can use it as "virtual" second account for your purposes without revealing your "actual" identity.

<p align ="center">Credits to **Groosha** for the actual version, I've simply added certain features which I thought were needed</p> <br>

 * [Prerequisites](#prerequisites)
 * [How to install](#how-to-install)
 * [What's new ?](#whats-new-)
 * [How it works ?](#how-it-works)
    * [Basic Functionality](#basic-functionality)
    * [Blocking and Unblocking Feature](#blocking-and-unblocking-feature)
    * [Available and Unavailable Feature](#available-and-unavailable-feature)
 * [Notes and restrictions](#notes-and-restrictions)
 * [Upcoming features](#upcoming-features)
 * [Remember](#remember)
 * [F.A.Q.](#faq)
 * [Contact](#contact)


 
## Prerequisites
* Python 3 (maybe works with Python 2, but I haven't tested it);
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/) library;
* Telegram account.
* Basic Knowledge about coding of course! 
* And the ability to read the manual patiently :D 

## How to install
* Get your own bot's token from [@BotFather](https://telegram.me/botfather);
* Find out your account's unique ID (you can use [ID bot](https://telegram.me/my_id_bot) or just send message via Curl or something else and get `message.chat.id` from response JSON);
* Fill in the necessary variables in `config.py`;
* Start bot: `python3 proxy_bot.py`

## What's new ???
* So I thought probably getting `/block~number~` and `/unblock~number~` after every text message was a bit annoying and it increases the number of text messages received, keeping this in mind I updated the bot. Now the admin can block a user by typing `/block @username/nickname` and to unblock by `/unblock @username/nickname`<br>
Details On how this works is down Under [Blocking and Unblocking Feature section](#blocking-and-unblocking-feature)
* Admins can now set their status as `/available` or `/unavailable`. This means that when you will not be available bot will notify the user if he/she tries to text you by sending him your unavailable message, just like the way you have a pre-recorded message on answering machines! The bot will however forward you the message. You can set and view your unavailable message by typing `/setunavailablemessage` and `/setunavailablemessage` respectively.
* You can now view the list of users you've blocked! By typing `/viewblocklist.` The list will contain their `@username/nickname`
* You can check your status whether you're currently available or unavailable by typing `/checkstatus`
* `/help` command is also there for admins to see all the available commands
* `/viewnicknames` to view all the nicknames of the users along with their first names.
* `/viewblockmessage` and `/setblockmessage` to view and set the block message that the user will see once he/she is blocked

## How it works
### Basic Functionality
The idea of this bot is pretty simple: you just place the bot between you and the one you want to chat with. The upside is that no one will find out your unique chat id or some other info (nickname, first name or avatar, for example). They won't also know your last seen time. However, the downside is that you can't initiate chat with someone (Because you're writing from bot and bots can't start chats to prevent spam), so you'll have to ask people to write to your bot first. Plus you will be only able to see their force replies in case they try to force reply one of the text in the private chat and not the actual text they forced reply to, in simple words..<br>  **Here's an example** : if a user force replies an image that was previously there in the chat with "what do you think about this picture up there ^ " then you will just receive the later text message and not the picture again.


<p align="center"> ![A simple scheme of interaction](https://habrastorage.org/files/4a2/d19/753/4a2d19753eb34073bfda0b872bf228b3.png)

<p align="center">![Screenshot](http://i.imgur.com/wVMZRgT.png)

### Blocking and Unblocking Feature
Alright, so after spending some time with the bot I thought `/block~number~` and `/unblock~number~` after every text was kinda annoying, so I updated the blocking feature in the bot. 
<br>
<br>
I thought that it would be probably **easier and less messy** if the admin can block a user based on the username.<br>
So, now you can block any user you want based on their @username or nickname provided by you, here's how it works:
<br>
<br>
Well, the bot simply stores the data of every user it interacts with in the form of a dictionary with the key as the Username and the val or value as the `message.chat.id` of the user. And therefore whenever the admin blocks a user by entering the username the bot simply takes in the username and gets the corresponding `chat.id` out of it and stores it in the block list.

Now some of you might be wondering like what if the user doesn't have a username or what if the user changed his/her username ?
Aye! we have a solution for that to but before answering that let's make a list of all the possible cases we can have.<br>
**There can be many possibilities and chances of error, I've made sure to cover all of them but who knows o_0**
 <br>
 <br>
**Okay!** So here are the cases: <br>
  
   **case 1:** user has a username and is a new user for the bot<br>
   **case 2:** user doesnt have a username and is a new user for the bot<br>
   **case 3:** user changed his username but is an old user for the bot<br>
   **case 4:** user removed his username and is an old user for the bot<br>
   **case 5:** idk that's it ? <br>
   <br>
   ``` python
    if message.chat.id not in user_dir.values():    
     if message.chat.username == None:
        msg = bot.send_message(config.my_id, "*Uh! the user does not have a username o_0*\nCan you please suggest a name that can be used to store the data of the following user ?\n *PS: The nickname should be unique and shouldn't contain* '`@`'",parse_mode="Markdown" )
        bot.register_next_step_handler(msg, lambda m: dictionary.process_name_step(m, dict_name=user_dir, file=config.storage_userdir, val=message.chat.id, firstname=message.chat.first_name))
           
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
                  bot.register_next_step_handler(msg, lambda m: dictionary.process_name_step(m, dict_name=user_dir, file=config.storage_userdir, val=message.chat.id, firstname=message.chat.first_name))
     else:
        userName = "@"+ message.chat.username
        userName = userName.lower()
        if userName not in user_dir:   
            dictionary.add_key_dict(config.storage_userdir, user_dir, userName, message.chat.id) 
```
**Alright so let's understand the code:**
```python
'''
 if message.chat.id not in user_dir.values() <-- here the bot checks whether the message.chat.id of the user exists in the dict or not
   if not: <--meaning it's a new user
     then it checks for the username
       if user doesnt have a username then ---> it asks the admin to give a nickname for the user to save that as key
       else it saves the username of the new user as the key and chat.id as the val
       We've successfully covere the cases 1 & 2 ^
   Now if message.chat.id is present in user_dir.values() 
   if yes: <---meaning its an old user 
      it then checks whether the username is present or not 
           if the user doesnt has a username (meaning the old user removed his/her username)
           then it cross checks in the dict whether the key of the user has '@' or not
               Now here's the tricky part: Why did I check for '@' ? Because in the case 2 we have given a nick name 
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
  '''
 ```
 
I hope this answered the questions and explained all the cases mentioned above, I know it's a bit complicated and a difficult way to code but idk i just didn't get any other idea. :P <br><br>
Since we know that no one is perfect in terms of recalling the previous data, I've included the `/viewnicknames` feature as well. This well help you to view all the nick-names along with the respective first-name of the user to whom it was allotted.<br><br>

So here are the following commands: <br>
* `/block @username/nickname`  <-- To **block** a user<br>
* `/unblock @username/nickname` <-- To **unblock** a user <br>
* `/setblockmessage` <-- To **set the block text** that the user will see once he/she is blocked <br>
* `/viewblockmessage` <-- To **view** your own block message
* `/viewnicknames` <-- To *view* all the allotted nicknames along with the user's first-name
<br>
**Admins can even view the block list by typing** `/viewblocklist` <br>

#### Screenshots:
#####Basic Blocking Functionality:
![screenshot](http://i.imgur.com/PSzgEDK.png)<br><br>
#####Setting the blocking text:
![screenshot](http://i.imgur.com/YwzUVEN.png)<br><br>
#####Viewing the Block List:
<p align="cente">![screenshot](http://i.imgur.com/CjC3S4M.png)<br><br>
####Setting and Viewing Nicknames:
<p align="center">![screenshot](http://i.imgur.com/E6gEQQY.png)<br><br>


### Available and Unavailable Feature
There can be at times when you as an admin are unavailable or don't temporarily have access to the bot, but you at the same time want to notify all the users about your unavailability just like the way we have on answering machines ? 
<br>
<br>
**"Joshua is Unavailable! Kindly leave your message after the beep.........."** 
<br>
<br>
Keeping this in mind here's the `/unavailable` and `/available` feature!
<br>
You can now set your status as **available** or **unavailable** <br>
<br>
So now the admins set the status by typing:
* `/available` <--- To set the status as available
* `/unavailable` <--- to set the status as unavailable<br>
To check the current status simply send `/checkstatus` to the bot<br><br>

If your status is set to **unavailable** then the bot will simply forward the message to the admin and notify the user about the unavailability of the admin **( by sending an unavailable message)**<br><br>
To set the unavailable message simply send:
* `/setunavailablemessage`

To view the unavailable message simply send:
* `/viewunavailablemessage`

####Screenshots :
##### Setting Unavailable Message :
![screenshot](http://i.imgur.com/sVznxXE.png)<br><br>
##### Basic Feature :
![screenshot](http://i.imgur.com/a4bZz3x.png)<br><br>
##### Checking Status:
<p align="center">![screenshot](http://i.imgur.com/KAtq778.png)<br><br>


## Notes and restrictions
1. Message formatting (both Markdown and HTML) is disabled. You can easily add `parse_mode` argument to `send_message` function to enable it.<br>
**example:**
``` python 
bot.send_message(message.chat.id, "Please click on [this](www.google.com)to search on Google",parse_mode="Markdown")
```

2. You(Admins) should **always** use "reply" function, because bot will check `message_id` of selected "message to reply".
3. Storage is needed to save `"message_id":"user_id"` key-value pairs. First, I intended to delete `message_id` which I've already answered, but then I decided to remove this, so you can answer any message from certain user and multiple times.
4. Supported message types in reply: `text`, `sticker`, `photo`, `video`, `audio`, `voice`, `document`, `location`.
5. To block a user simply type`/block @username/nickname` and to unblock a user simply type `/unblock @username/nickname`
6. If you dont need these features then you can simply use the original version of the bot which was made by Groosha. Open the terminal and enter `python3 original_proxy_bot.py`
7. All the text files are mentioned in config.py except **blank.txt** which is used somewhere in between the code.<br>
** I will not recommend you to change the name or the location of the text files. But it's up to you! **
8. This bot only works in the private chats, I've tried making it work in the groups but it didn't really worked, if you can improve this bot then do let [me](https://telegram.me/mrgigabytebot) know! I would be glad to make this work better

## Upcoming Features
* I would be working on adding some more helpful features for admins and maybe for the users as well let's see :)
* Anti-Spam Feature, limiting messages sent per-second
* Broadcast feature for admins, they can broadcast a certain message to selected users they want
* idk maybe more ?? haha

## Remember!
I understand, that "proxy" bots can be used to prevent spammers from being reported, so if you encounter such bots that are used to do "bad" things, feel free to report them: [abuse@telegram.org](mailto:abuse@telegram.org)

## F.A.Q
#### 1. Will this bot work in groups/supergroups/channels ?
For the time being this bot just works in private chats.

#### 2. Can I use Emojis in my unavailable message ?
Yes! You can use **ONLY** emojis or text in your unavailable message, you cannot save stickers/gifs in the unavailable message

#### 3. Will I be able to skip my school/college/job ? 
Unfortunately nope :( 

## Contact
You can contact me via my [Proxy Bot](https://telegram.me/mrgigabytebot).<br>
**PS: Let me know if you need a new feature/tweak in this bot, please don't hesitate to text me :)**
