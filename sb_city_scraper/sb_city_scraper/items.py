# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Meeting object for city meetings 
class Meeting(scrapy.Item):
    Groups = scrapy.Field()
    Type = scrapy.Field()
    Date = scrapy.Field()
    Time = scrapy.Field()
    Location = scrapy.Field()
    Info = scrapy.Field()


# Library object for city events 
class LibraryEvent(scrapy.Item):
    Event = scrapy.Field()
    Location = scrapy.Field()
    Date = scrapy.Field()
    Time = scrapy.Field()
    Desc = scrapy.Field()     
    
# News Item object for sb police news
class NewsItem(scrapy.Item):
    Title = scrapy.Field()
    Date = scrapy.Field()
    Desc = scrapy.Field()
    Read_more = scrapy.Field()