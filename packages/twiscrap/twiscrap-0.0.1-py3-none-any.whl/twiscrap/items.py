from scrapy import Field, Item


class Tweet(Item):
    id_ = Field()
    raw_data = Field()


class User(Item):
    id_ = Field()
    raw_data = Field()
