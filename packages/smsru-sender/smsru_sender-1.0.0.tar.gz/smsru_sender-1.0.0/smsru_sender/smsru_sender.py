# encoding=utf-8

"""An sms.ru client.

Provides a class that lets you use sms.ru API to send message and verify its status.

Configuration is looked in .env file at the project root.
Example config for simple auth:

  SMSRU_API_ID=00000000-0000-0000-0000-000000000000
  SENDER_NAME=MyName

To use in a Python program:

  from smsru_sender import SMSruSender
  smsru = SMSruSender()
  smsru.send("+79112223344", "Hello world")

"""

import logging
import os
from copy import copy

import requests
from dotenv import load_dotenv

from .exceptions import *
from .request_response import RequestResponse

logger = logging.getLogger(__name__)
load_dotenv()

__author__ = "Egor Gvozdikov"
__email__ = "work.egvo@ya.ru"
__all__ = ["SMSruSender"]


class SMSruSender(object):
    def __init__(self, api_id='', sender='', raise_exc=True):
        if not api_id:
            api_id = os.getenv('SMSRU_API_ID', '')
            if not api_id:
                logger.error("API id is not specified.")
                if raise_exc:
                    raise NotConfigured("API id is not specified.")
        if not sender:
            sender = os.getenv('SMSRU_SENDER', '')
        self.url = 'https://sms.ru/sms/send'
        self.api_id = api_id
        self.sender = sender
        self.params_template = {'api_id': self.api_id, 'json': '1'}
        self.raise_exc = raise_exc

    def send(self, to, message, express=False, test=False):
        """Sends the message to the specified recipient. Returns a numeric
        status code, its text description and, if the message was successfully
        accepted, its reference number."""
        if not isinstance(message, str):
            raise ValueError("Message must be a unicode")
        params = copy(self.params_template)
        params.update({"to": to, "text": message})
        if self.sender:
            params["from"] = self.sender
        if express:
            params["express"] = "1"
        if test:
            params["test"] = "1"
        response = requests.get(self.url, params=params)
        return RequestResponse(response)
