# TODO: add a readme with needed docs

class BaseApi:
    def call_api(self):
        raise NotImplementedError("Subclasses must implement call_api method")
    
    def filter_articles(self):
        raise NotImplementedError("Subclasses must implement filter_articles method")