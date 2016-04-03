# Telegram Proxy Bot 
`Credits for the original version of this bot goes to` **Groosha** `, I've simply added certain features which I thought were needed` <br>
A simple BITM (bot-in-the-middle) for [Telegram](https://telegram.org/) acting as some kind of "proxy". You can use it as "virtual" second account for your purposes revealing your "real" identity.  

## Prerequisites
* Python 3 (maybe works with Python 2, but I haven't tested it);
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/) library;
* Telegram account.
* Basic Knowledge about coding of course! ( and the ability to read the manual patiently :D )

## How to install
* Get your own bot's token from [@BotFather](https://telegram.me/botfather);
* Find out your account's unique ID (you can use [My ID bot](https://telegram.me/my_id_bot) or just send message via Curl or something else and get `Message.chat.id` from response JSON);
* Fill in the necessary variables in `config.py`;
* Start bot: `python3 proxy_bot.py`


## How it works

The idea of this bot is pretty simple: you just place the bot between you and the one you want to chat with. The upside is that no one will find out your unique chat id or some other info (nickname, first name or avatar, for example). They won't also know your last seen time. However, the downside is that you can't initiate chat with someone (Because you're writing from bot and bots can't start chats to prevent spam), so you'll have to ask people to write to your bot first. Plus you will be only able to see their force replies in case they try to force reply one of the text in the private chat and not the actual text they forced reply to, in simple words..<br>  **Here's an example** : if a user force replies an image that was previously there in the chat with "what do you think about this picture up there ^ " then you will just receive the later text message and not the picture again.

![A simple scheme of interaction](https://habrastorage.org/files/4a2/d19/753/4a2d19753eb34073bfda0b872bf228b3.png)

![](http://i.imgur.com/hBCedtS.png)
<hr>
<br>

## Blocking Feature:
![](http://i.imgur.com/vW6d7fm.png)

## Improved features! 
* The user can now see whether you're typing a text, or sending an audio or simply uploading a video (inclusion of `send_chat_action` method);
* **Blocking feature!** Getting annoyed by some users ? Don't know how to prevent them for texting your bot ? Here's the blocking feature just for you! You can now block the users you want and you wont receive any updates from them via your bot;



## Notes and restrictions

1. Message formatting (both Markdown and HTML) is disabled. You can easily add `parse_mode` argument to `send_message` function to enable it.
2. You should **always** use "reply" function, because bot will check `message_id` of selected "message to reply".
3. Storage is needed to save `"message_id":"user_id"` key-value pairs. First, I intended to delete `message_id` which I've already answered, but then I decided to remove this, so you can answer any message from certain user and multiple times.
4. Supported message types in reply: `text`, `sticker`, `photo`, `video`, `audio`, `voice`, `document`, `location`.
5. To block a user simply tap `/block~message.chat.id~` and to unblock a user simply tap `/unblock~message.chat.id~`
6. Since it's not possible to make changes in the forwarded text and concat the /block and /unblock command all in one(as for now) it might happen that you might get annoyed because of the repeated texts, keeping that in mind you can simply use the original version of the bot which was made by Groosha. Open the terminal and enter `python3 original_proxy_bot.py`
7. The Original Text file for saving all the details of the blocked user is `chatids.txt` but you can change that file to some other name if you want.(should be a text file only!)

## Remember!
I understand, that "proxy" bots can be used to prevent spammers from being reported, so if you encounter such bots that are used to do "bad" things, feel free to report them: [abuse@telegram.org](mailto:abuse@telegram.org)


## Contact
You can contact me via my [Proxy Bot](https://telegram.me/mrgigabytebot).<br>
**PS: Let me know if you need a new feature/tweak in this bot, please don't hesitate to text me :)**
