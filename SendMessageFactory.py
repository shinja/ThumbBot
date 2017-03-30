import re

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


class URLFactory:

    # static variable
    imgur_regex = re.compile(url_protocol_regex + '((i\.imgur\.com\/)([\w]+)(\.(jpg|png|gif)))')

    def __init__(self, url):
        self.url = url #instance variable
    
    def getSendMessageInstance(self):

        matches = self.imgur_regex.search(self.url)
        if matches:

           original_content_url = 'https://%s' % (matches.group(1))
           preview_image_url = 'https://%s%s%s' % (matches.group(2), matches.group(3) + 'm', matches.group(4))

           image_message = ImageSendMessage(original_content_url=original_content_url, preview_image_url=preview_image_url)
           return image_message
    