# -*- coding: utf-8 -*-

import time
import json
import logging
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

from django.conf import settings

from core.utils import parse_message


SLEEP = 15 # seconds
LOG = logging.getLogger("streaming")
URL = "http://{ip}:{port}/api/tweet/?username={username}&api_key={api_key}".format(
    **settings.STREAM_API_CREDENTIALS["default"]
    )


class TwitterListener(StreamListener):
    def __init__(self, processor, *args, **kwargs):
        if processor is not None:
            self.processor = processor
        else:
            self.processor = print
        super().__init__(*args, **kwargs)

    def on_data(self, data):
        self.processor(json.loads(data))
        return True

    def on_error(self, status):
        LOG.error(status)
        if status == 420:
            # Returning False in on_data disconnects the stream
            return False

    def on_timeout(self):
        LOG.warning("Timeout, sleeping for {} seconds...".format(SLEEP))
        time.sleep(SLEEP)
        return


class TwitterStream(Stream):
    def __init__(self, processor, *args, **kwargs):
        """
        Handles Twitter authetification and the connection
        to Twitter Streaming API.

        :kwarg consumer_key: str
        :kwarg consumer_secret: str
        :kwarg access_token: str
        :kwarg access_token_secret: str
        """
        consumer_key = kwargs.get(
            'consumer_key',
            settings.TWITTER_CONSUMER_KEY
            )
        consumer_secret = kwargs.get(
            'consumer_secret',
            settings.TWITTER_CONSUMER_SECRET
            )
        access_token = kwargs.get(
            'access_token',
            settings.TWITTER_ACCESS_TOKEN
            )
        access_token_secret = kwargs.get(
            'access_token_secret',
            settings.TWITTER_ACCESS_TOKEN_SECRET
            )
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.listener = TwitterListener(processor=processor)
        super().__init__(self.auth, self.listener)
