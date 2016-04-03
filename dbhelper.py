# -*- coding: utf-8 -*-
# A simple wrapper on Python 3 Shelve module
# https://docs.python.org/3.5/library/shelve.html

import shelve
import config

def add_message(message_id, user_id):
    """
    Add key `message_id` with value `user_id`
    Integers can't be keys in Shelve, so we convert them to strings
    :param message_id: :param message_id: Telegram Message unique ID (within bot)
    :param user_id: User's unique ID
    """
    with shelve.open(config.storage_name) as db:
        db[str(message_id)] = user_id

# Temporally not using this to allow you to answer the same user multiple times
# and/or use ANY message from certain user to write to him
def delete_message(message_id):
    """
    Remove unnecessary key-value pair from Shelve to keep storage as small as possible
    :param message_id: Telegram Message unique ID (within bot)
    """
    with shelve.open(config.storage_name) as db:
        del db[str(message_id)]


def get_user_id(message_id):
    """
    Get user_id for given message_id
    On error, None is returned
    :param message_id:
    :exception KeyError: No key found with name "message_id"
    :return: User's unique ID on success / None if error occurs
    """
    try:
        with shelve.open(config.storage_name) as db:
            return db[str(message_id)]
    except KeyError:
        return None
