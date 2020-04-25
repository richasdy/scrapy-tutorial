# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime


def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip(u'\u201c'u'\u201d')
    return text


def convert_date(text):
    # convert string March 14, 1879 to Python date
    return datetime.strptime(text, '%B %d, %Y')


def parse_location(text):
    # parse location "in Ulm, Germany"
    # this simply remove "in ", you can further parse city, state, country, etc.
    return text[3:]


class FileItem(Item):
    header = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    url = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    images = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    image_urls = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    files = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    file_urls = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
