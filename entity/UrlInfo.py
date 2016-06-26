

class UrlInfo():
    key = 0
    title = ''
    url = ''
    description = ''
    vote = 0

    def __init__(self, key, title, url, description, vote):
        self.key = key
        self.title = title
        self.url = url
        self.description = description
        self.vote = vote