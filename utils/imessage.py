import sqlite3
from os.path import expanduser
from operator import itemgetter


MESSAGES_FROM_ME_QUERY = 'SELECT `text` FROM message WHERE `is_from_me` = 1'


def get_messages_from_me():
    """
    Get all "from me" iMessages in the current users's chat db.
    """
    with sqlite3.connect(expanduser('~/Library/Messages/chat.db')) as conn:
        return map(itemgetter(0), conn.execute(MESSAGES_FROM_ME_QUERY))
