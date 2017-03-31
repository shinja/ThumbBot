import re
from URLPattern import URLPattern

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage, ImageSendMessage
)

url_protocol_regex = '^https?:\/\/'

class SendMessageFactory:

    def __init__(self):
        pass
    
    def getSendMessageInstance(self, text=None):

        if re.search(url_protocol_regex, text):
            return URLFactory(text).getSendMessageInstance()

        return None 



def imgur_handler(matches):
    original_content_url = 'https://%s' % (matches.group(1))
    preview_image_url = 'https://%s%s%s' % (matches.group(2), matches.group(3) + 'm', matches.group(4))

    image_message = ImageSendMessage(original_content_url=original_content_url, preview_image_url=preview_image_url)
    return image_message

def youtube_handler(matches):
    
    id = matches.group(2)

    original_content_url = 'https://img.youtube.com/vi/%s/hqdefault.jpg' % (id)
    preview_image_url = 'https://img.youtube.com/vi/%s/mqdefault.jpg' % (id)

    image_message = ImageSendMessage(original_content_url=original_content_url, preview_image_url=preview_image_url)
    return image_message

class URLFactory:

    # static variable
    patterns = [
        URLPattern(url_protocol_regex + '((i\.imgur\.com\/)([\w]+)(\.(jpg|png|gif)))', imgur_handler),
        URLPattern(url_protocol_regex + '.*youtu\.?be.*\/(watch\?v=)?([\w]+)', youtube_handler)
    ]

    def __init__(self, url):
        self.url = url #instance variable
    
    def getSendMessageInstance(self):

        for pattern in self.patterns:

            msg = pattern.getSendMessageInstance(self.url)
            if msg:
                return msg
        