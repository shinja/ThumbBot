import re

class URLPattern:

    def __init__(self, regex, func):

        self.regex = re.compile(regex)
        self.func = func
    
    def getSendMessageInstance(self, url):

        matches = self.regex.search(url)
        if matches:
            return self.func(matches)

        return None
