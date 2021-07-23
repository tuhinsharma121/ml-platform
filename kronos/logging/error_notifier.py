import sys
import traceback

import requests

from config import *


def send_notification(message):
    """Sends notification to telegram
    Parameters
    ----------
    message: str
        The message to be sent to Telegram

    Returns
    -------
        response : `Response <Response>` object
    """
    subject = DEPLOYMENT_TYPE + "-" + CODE_BASE + "-error : "
    text = "```\n{sub}\n\n{msg}\n```".format(sub=subject, msg=message)
    response = requests.post(TELEGRAM_URL,
                             data={
                                 "chat_id": TELEGRAM_CHANNEL_ID,
                                 "text": text,
                                 "parse_mode": "Markdown"})

    return response


def get_error_stack_trace():
    """Gets the system stacktrace during an exception is occured. It is useful to use in Exception block.
    Returns
    -------
        stack_trace: str
            Returns the stacktrace
    """
    e_type, e_name, e_traceback = sys.exc_info()
    stack_trace = e_type.__name__ + " ( " + str(e_name) + " ) " + "\n\n" + "".join(traceback.format_tb(e_traceback))
    return stack_trace
